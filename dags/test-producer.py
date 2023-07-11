from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

test_file = Dataset("/opt/airflow/dags/files/employees.csv")

with DAG (
    dag_id = "producer",
    schedule="@daily",
    start_date =datetime(2022,1,1),
    catchup = False
):


    @task()
    def update_test_file():
        with open(test_file.uri, "a+") as f:
            f.write("97,TEST,TEST,ACK,0")

    update_test_file()
