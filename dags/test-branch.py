import os
import sys

#  it's required to work in Airflow with packages
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from datetime import datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

def branch_fn():
    #return "t5"  # id of the next task
    return "t4"


with DAG (
    dag_id="test-branch",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
):
    t1 = DummyOperator(task_id="t1")
    t2 = DummyOperator(task_id="t2")
    t3 = BranchPythonOperator(task_id="t3", python_callable=branch_fn)
    t4 = DummyOperator(task_id="t4")
    t5 = DummyOperator(task_id="t5")
    t6 = DummyOperator(task_id="t6")
    # default TriggerRule = ALL_SUCCESS
    # It means that the task will run if all parents have succeeded
    t7 = DummyOperator(task_id="t7", trigger_rule=TriggerRule.ONE_SUCCESS)
    t8 = DummyOperator(task_id="t8")
    t9 = DummyOperator(task_id="t9")

    t1 >> t2 >> t3
    t3 >> t4
    t3 >> t5 >> t6
    t4 >> t7
    t6 >> t7
    t7 >> t8 >> t9