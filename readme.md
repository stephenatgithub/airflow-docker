# Airflow

A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.



# Docker

- Fetching docker-compose.yaml

`curl -LfO "https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml"`


- Create directories 

`mkdir -p ./dags ./logs ./plugins ./config`


- Create environment variables

`AIRFLOW_UID=50000`


- Initialize the database

`docker compose up airflow-init`

- Running Airflow

`docker compose up`


# Scheduler

For DAGs with a cron or timedelta schedule, scheduler won’t trigger your tasks until the period it covers has ended.

e.g., A job with schedule set as @daily runs after the day has ended. 

This technique makes sure that whatever data is required for that period is fully available before the DAG is executed. In the UI, it appears as if Airflow is running your tasks a day late

The scheduler runs your job one schedule AFTER the start date, at the END of the interval.


# Features

- schedule with dataset
- ETL
- send email


# Use Case

1. event drive by new file (trade feed/ price feed)

2. generate reports and send emails

3. manage job dependencies 






