from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.smtp.notifications.smtp import send_smtp_notification

FROM_EMAIL=""
TO_EMAIL=""

def send_email(subj, cont):
    return send_smtp_notification(
        from_email=FROM_EMAIL,
        to=TO_EMAIL,
        subject=subj,
        html_content=cont,            
    )

with DAG(
    dag_id="test-notifier",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
):
    task = BashOperator(
        task_id="bash_oper",
        bash_command="echo xxx",
        on_success_callback=[send_email("[Success] bash_oper finished", "done")],
        on_failure_callback=[send_email("[Error] bash_oper failed", "debug logs")],
    )

    task    