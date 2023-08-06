from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator


with DAG (
    default_args={
        'owner': 'airflow',
        'do_xcom_push': True,
    },
    dag_id="test-api",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
):
    t1 = SimpleHttpOperator(
        task_id='test-api-get',
        method='GET',
        http_conn_id='http_default',
        endpoint='',
        headers={"Content-Type": "application/json"},
        
    )

    t1

