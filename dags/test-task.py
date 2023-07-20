from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator


# 所有工作都可以分享這一套設定
default_args = {
  	# 列明工作的擁有人
    'owner': 'airflow',
  	# 發送警示電郵的對象
    'email': ['fake_email@gmail.com'],
  	# 在工作重試時發出電郵
    'email_on_retry': False,
  	# 在工作失敗時發出電郵
    'email_on_failure': True,
    # 宣告工作失敗前可重試次數
    'retries': 1,
    # 工作重試開始前的等待時間
    'retry_delay': timedelta(seconds=10),
  	# 工作開始的日子
    'start_date': datetime(2021, 6, 15, 0, 0, 0, 0),
  	# 工作預算的工作時長，若超過則用電郵通知
  	'sla': timedelta(seconds=10),
    # 過長則中止並令工作失敗
  	'execution_timeout': timedelta(minutes=5),
  	# 把此工作訊息傳給其他工作
    'do_xcom_push': True,
}

with DAG(
  	# DAG 的名字
    'test-task',
  	# DAG 的描述，可以在 UI 看到
    description='A DAG for demonstration',
  	# DAG 的執行間隔
  	schedule_interval="@once",
  	# DAG 的開始時間，第一次執行會是 start_date + schedule_interval
  	start_date=datetime(2021, 7, 1, 0, 0, 0, 0),
    catchup=False,
  	# DAG 下工作的基礎設定
    default_args=default_args,
  	# 搜尋用標籤
    tags = ['Testing', 'Tutorial'],
) as dag:
    start = DummyOperator(
        task_id='start',
    )
    
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo 1',
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='echo 2',
    )

    task_confirm = BashOperator(
        task_id='task_confirm',
        bash_command='echo "task_1 and task_2 completed"'
    )
        
    end = DummyOperator(
        task_id='end',
    )

    start >> [task_1, task_2] >> task_confirm >> end