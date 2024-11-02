#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import sys
import logging
import duckdb
import time
from typing import List, Dict, Any

# Function to get tasks without pagination
def extract_dependencies(base_url: str, dag_ids: list[str], dag_run_id: str, auth: HTTPBasicAuth) -> List[List[str]]:
    """Extract dependencies for the specified DAG"""

    dependencies = []

    assert type(dag_ids) is list

    for dag_id in dag_ids:
        endpoint = f"{base_url}/api/v1/dags/{dag_id}/tasks"
        logging.info(f"Extracting dependencies for dag {dag_id} from endpoint: {endpoint}")
        
        # Make request for all tasks
        response = requests.get(endpoint, auth=auth)
        
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.text}")

        if response.status_code != 200:
            logging.error(f"Error: Unable to fetch tasks for DAG {dag_id}. Status code: {response.status_code}")
            logging.error(f"Response content: {response.text}")
            sys.exit(1)

        tasks = response.json()['tasks']

        logging.info(f"Found {len(tasks)} tasks for dependency analysis")
        
        for task in tasks:
            for downstream_task in task['downstream_task_ids']:
                dependencies.append([dag_id, task['task_id'], dag_id, downstream_task])
            if task['class_ref']['class_name'] == "ExternalTaskSensor":
                task_instance_endpoint = f"{base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task['task_id']}"

                logging.info(f"Extracting upstream information for ExternalTaskSensor task {task['task_id']} from endpoint: {task_instance_endpoint}")
                response = requests.get(task_instance_endpoint, auth=auth)
                task_info = response.json()

                if 'rendered_fields' in task_info and 'external_dag_id' in task_info['rendered_fields'] and 'external_task_id' in task_info['rendered_fields']:
                    external_dag_id = task_info['rendered_fields']['external_dag_id']
                    external_task_id = task_info['rendered_fields']['external_task_id']

                    dependencies.append([external_dag_id, external_task_id, dag_id, task['task_id']])
                else:
                    logging.warning(f"Could not find upstream information for ExternalTaskSensor task {task['task_id']} from endpoint: {task_instance_endpoint} for dag_run_id {dag_run_id}")
    
        logging.info("Sleeping to throttle requests...")
        time.sleep(3)

    return dependencies


# Updated function to output dependencies (DuckDB only)
def load_dependencies(dependencies: List[List[str]], db_path: str) -> None:
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dependencies (
            upstream_dag_id VARCHAR,
            upstream_task_id VARCHAR,
            downstream_dag_id VARCHAR,
            downstream_task_id VARCHAR
        )
    """)
    
    # Validate dependencies
    for dep in dependencies:
        if len(dep) != 4:
            raise ValueError(f"Invalid dependency: {dep}. Expected 4 elements, got {len(dep)}.")
    
    conn.executemany("""
        INSERT INTO dependencies (upstream_dag_id, upstream_task_id, downstream_dag_id, downstream_task_id)
        VALUES (?, ?, ?, ?)
    """, dependencies)
    conn.close()
    logging.info(f"Dependencies written to DuckDB at {db_path}")

def etl_dependencies(base_url: str, dag_ids: list[str], dag_run_id: str, auth: HTTPBasicAuth, output_file: str) -> None:
    logging.info(f"Starting to fetch dependencies for DAGs: {dag_ids} from base URL: {base_url}")
    dependencies = extract_dependencies(base_url, dag_ids, dag_run_id, auth)
    load_dependencies(dependencies, output_file)
    logging.info(f"Finished extracting dependencies for DAGs: {dag_ids}")

# Function to get task instances
def extract_task_instances(base_url: str, dag_ids: list[str], dag_run_id: str, auth: HTTPBasicAuth, page_length: int = 100) -> List[Dict[str, Any]]:
    """Extract all task instances for the specified dag_id and dag_run_id"""

    assert type(dag_ids) is list

    all_task_instances = []

    for dag_id in dag_ids:
        def get_response():
            endpoint = f"{base_url}/api/v1/dags/~/dagRuns/~/taskInstances/list"
            logging.info(f"Fetching {dag_id} task instances from: {endpoint}")
        
            params = {
                "dag_ids": [dag_id],
                "dag_run_ids": [dag_run_id]
            }
            response = requests.post(endpoint, auth=auth, json=params)
            
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.text}")

            return response 
        
        response = get_response()

        if response.status_code != 200: 
            logging.warning("Received error from API. Waiting 120 seconds and retrying.")
            time.sleep(120)
            response = get_response()

            if response.status_code != 200:
                logging.error(f"Error: Unable to fetch task instances. Status code: {response.status_code}")
                logging.error(f"Response content: {response.text}")
                sys.exit(1)

        data = response.json()
        dag_task_instances = data['task_instances']
        for ti in dag_task_instances:
            if ti['operator'] == "ExternalTaskSensor":
                # If this is an ExternalTaskSensor, we consider this task to run 
                # instantly rather than starting at beginning of dag run. This 
                # makes the Ready time and Running time for this task more accurate.
                ti['start_date'] = ti['end_date']
        
        logging.info(f"Finished fetching all task instances for dag {dag_id}. Total: {len(dag_task_instances)}")

        all_task_instances.extend(dag_task_instances)

        logging.info("Sleeping to throttle requests...")
        time.sleep(3)
    
    logging.info(f"Finished fetching all task instances. Total: {len(all_task_instances)}")

    return all_task_instances


# Updated function to output task instances (DuckDB only)
def load_task_instances(task_instances: List[Dict[str, Any]], db_path: str) -> None:
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_instances (
            task_id VARCHAR,
            task_display_name VARCHAR,
            dag_id VARCHAR,
            dag_run_id VARCHAR,
            execution_date TIMESTAMP,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            duration FLOAT,
            state VARCHAR,
            try_number INTEGER,
            map_index INTEGER,
            max_tries INTEGER,
            hostname VARCHAR,
            unixname VARCHAR,
            pool VARCHAR,
            pool_slots INTEGER,
            queue VARCHAR,
            priority_weight INTEGER,
            operator VARCHAR,
            queued_when TIMESTAMP,
            pid INTEGER,
            executor VARCHAR,
            executor_config VARCHAR,
            rendered_fields VARCHAR,
            note VARCHAR
        )
    """)
    
    columns = ['task_id', 'task_display_name', 'dag_id', 'dag_run_id', 'execution_date',
               'start_date', 'end_date', 'duration', 'state', 'try_number', 'map_index',
               'max_tries', 'hostname', 'unixname', 'pool', 'pool_slots', 'queue',
               'priority_weight', 'operator', 'queued_when', 'pid', 'executor',
               'executor_config', 'rendered_fields', 'note']
    
    prepared_data = [[ti.get(col) for col in columns] for ti in task_instances]
    
    conn.executemany(f"""
        INSERT INTO task_instances ({','.join(columns)})
        VALUES ({','.join(['?' for _ in columns])})
    """, prepared_data)
    
    conn.close()
    logging.info(f"Task instances written to DuckDB at {db_path}")

# Updated function to extract task instances
def etl_task_instances(base_url: str, dag_ids: list[str], dag_run_id: str, auth: HTTPBasicAuth, output_file: str, page_lenth: int = 100) -> None:
    logging.info(f"Starting to fetch task instances for DAGs: {dag_ids}, DAG Run: {dag_run_id} from base URL: {base_url}")
    task_instances = extract_task_instances(base_url, dag_ids, dag_run_id, auth, page_lenth)
    load_task_instances(task_instances, output_file)
    logging.info(f"Finished extracting task instances for DAGs: {dag_ids}, DAG Run: {dag_run_id}")


def get_all_dag_ids(base_url: str, auth: HTTPBasicAuth) -> list[str]:
    """Retrieve all DAGs in the environment and return a list of dag_ids."""
    endpoint = f"{base_url}/api/v1/dags"
    all_dag_ids = []
    limit = 100
    offset = 0

    while True:
        params = {
            'limit': limit,
            'offset': offset
        }
        response = requests.get(endpoint, auth=auth, params=params)
        
        if response.status_code != 200:
            logging.error(f"Error: Unable to fetch DAGs. Status code: {response.status_code}")
            logging.error(f"Response content: {response.text}")
            sys.exit(1)

        data = response.json()
        dags = data['dags']
        
        if not dags:
            break

        all_dag_ids.extend([dag['dag_id'] for dag in dags])
        
        if len(dags) < limit:
            break

        offset += limit
        logging.info(f"Fetched {len(all_dag_ids)} DAGs so far. Continuing to next page...")

    logging.info(f"Finished fetching all DAGs. Total: {len(all_dag_ids)}")
    return all_dag_ids
