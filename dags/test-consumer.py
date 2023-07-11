from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

test_file = Dataset("/opt/airflow/dags/files/employees.csv")

with DAG(
    dag_id="consumer",
    schedule=[test_file],
    start_date=datetime(2022,1,1),
    catchup=False
):

    @task
    def read_test_file():
        with open(test_file.uri, "r") as f:
            print(f.read())

    read_test_file()