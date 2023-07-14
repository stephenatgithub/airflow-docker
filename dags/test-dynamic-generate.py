#* DAG related packages
from airflow import DAG

#* Time-related packages
from datetime import datetime   # Declare date time
from datetime import timedelta  # Declare the change of time
import pendulum                 # Declare timezone

#* CSV Reader
import csv

#* Directory nagivation
import pathlib

#* Airflow Operators and Hooks
from airflow.providers.ssh.operators.ssh    import SSHOperator
from airflow.operators.dummy                import DummyOperator

# Set the timezone, otherwise it might be UTC
local_tz = pendulum.timezone("Asia/Hong_Kong")

# The function that create dag
def _create_dag(row):
    default_args = {
        'owner': 'airflow',
        'email': ['fake_email@gmail.com'],
        'email_on_retry': False,
        'email_on_failure': True,
        'retries': 1,
        'retry_delay': timedelta(seconds=10),
        'start_date': datetime(2021, 7, 15, 0, 0, 0, 0),
        'sla': timedelta(seconds=10),
        'execution_timeout': timedelta(minutes=5),
        'do_xcom_push': True,
    }

    with DAG(
        row['report_name'],
        default_args=default_args,
        start_date=datetime(2021, 7, 12, 0, 0, 0, 0, tzinfo = local_tz),
        schedule_interval=row['cron_expression'],
        catchup = False,
        tags = ['Medium', 'Dynamic-DAG'],
    ) as dag:

        start = DummyOperator(
            task_id='Start',
        )

        run_command = SSHOperator(
            task_id = 'Generate_Report',
            ssh_conn_id = row['connection_name'],
            command = row['command'],
        )

        end = DummyOperator(
            task_id='End',
        )

        start >> run_command >> end

        dag.doc_md = f"""
        # {row['report_name']}
        This report will run command "{row['command']}" using connection ID: {row['connection_name']}.
        """

    return dag

data_path = "/opt/airflow/dags/files/report_list.csv"
#src_path = pathlib.Path(__file__).parent.resolve()
#with open(f'{src_path}/.src/report_list.csv', newline='') as csvfile:
with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      globals()[row['report_name']] = _create_dag(row)