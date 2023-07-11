from datetime import datetime as dt
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
'start_date' : days_ago(1),
'retries' : 1,
'retry_delay' : timedelta(minutes=5)
}

dag = DAG('hello_world_dag',
    description = 'Simple Hello World DAG',
    default_args = default_args,
    schedule_interval = timedelta(days = 1)
)

def print():
    return ("Hello world")

task = PythonOperator(
  task_id = 'print_hello_world',
 python_callable = print,
 dag = dag)

task