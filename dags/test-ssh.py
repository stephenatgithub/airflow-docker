# DAG related packages
from airflow import DAG
from datetime import datetime   # Declare date time
from datetime import timedelta  # Declare the change of time
import pendulum                 # Declare timezone

# Function related packages
import base64                   # SSHOpearator decode
import logging                  # Replace print to look more professional

# Operators
from airflow.operators.python               import PythonOperator
from airflow.providers.ssh.operators.ssh    import SSHOperator
from airflow.operators.dummy                import DummyOperator

# Exceptions
from airflow.exceptions                     import AirflowFailException

# Set the timezone, otherwise it might be UTC
local_tz = pendulum.timezone("Asia/Hong_Kong")

def _decode_message(task_name, ti):
    """Decode base64 xcom output from SSHOperator"""
    message = ti.xcom_pull(task_ids=task_name)
    print(message)
    return base64.b64decode(message).decode()

def _validate_job(task_name, threshold, ti):
    """Fail the job if the decoded number is smaller than threshold"""
    number = int(ti.xcom_pull(task_ids=task_name))
    logging.info(f"Number generated is: {number}")
    if number < threshold:
        raise AirflowFailException(f"Number {number} is smaller than threshold {threshold}, unlucky.")
    else:
        logging.info(f"NUmber {number} is larger than or equal to threshold {threshold}, job continues.")
    
default_args = {
    'owner': 'airflow',
    'email': ['fake_email@gmail.com', 'fake_email_2@gmail.com'],
    'email_on_retry': False,
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
    'start_date': datetime(2021, 7, 10, 0, 0, 0, 0, local_tz),
    'do_xcom_push': True
}

with DAG(
    'test-ssh',
    default_args=default_args,
    start_date=datetime(2021, 7, 10, 0, 0, 0, 0, tzinfo = local_tz),
    schedule_interval=None,
    tags = ['Medium'],
    catchup = False,
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    ssh = SSHOperator(
        task_id='ssh',
        ssh_conn_id='ssh',
        command='echo 123000',
    )
    decode = PythonOperator(
        task_id='decode',
        python_callable=_decode_message,
        op_args=[
            'ssh',
        ],
    )
    validate = PythonOperator(
        task_id='validate',
        python_callable=_validate_job,
        op_args=[
            'decode',
            10000,
        ]
    )
    start >> ssh >> decode >> validate >> end