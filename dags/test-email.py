from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retires': 1,
    'retry_delay': timedelta(seconds=5),
    # receipion email
    'email': '',
    # overwrite default value in airflow.cfg
    'email_on_failure': True,
    'email_on_retry': True
}

with DAG (
    dag_id = "test-email",
    start_date = datetime(2023,5 ,1),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags = ['Testing', 'Email'],
) as dag:
    task1 = BashOperator(
        task_id='bash_task',
        bash_command='cd xxxx'
    )

    task1