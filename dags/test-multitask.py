from datetime import datetime
from typing import List

from airflow import DAG
from airflow.decorators import task
from airflow.models.taskinstance import LazyXComAccess

@task
def get_file_names() -> List[str]:
    import random

    random_number = random.randint(0, 10)
    return [f'{n + 1}.txt' for n in range(random_number)]

@task
def process_file_name(file_name: str) -> str:
    return file_name.replace('.txt', '.json')

with DAG(dag_id="test-multitask", start_date=datetime(2022, 9, 14),schedule_interval="@once",catchup=False) as dag:
    file_names = get_file_names()
    processed_file_names = process_file_name.expand(file_name=file_names)    