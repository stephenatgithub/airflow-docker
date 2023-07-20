# Airflow

A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.



# Docker

- Fetching docker-compose.yaml

`curl -LfO "https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml"`


- Create directories 

`mkdir -p ./dags ./logs ./plugins ./config`


- Create environment variables

`AIRFLOW_UID=50000`


- Initialize airflow 

`docker compose up airflow-init`

> docker-compose is old syntax.

- Running Airflow

`docker compose up`

- Execute a command in a running container

`docker exec --user root -it <container> bash`
> --interactive , -i		Keep STDIN open even if not attached
> --tty , -t		Allocate a pseudo-TTY

- check current user 

`whoami`


- Additional Dependencies 

[Using custom images](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#using-custom-images)

[Adding new PyPI packages individually](https://airflow.apache.org/docs/docker-stack/build.html#adding-new-pypi-packages-individually)


1. create Dockerfile alongside docker-compose.yaml (under same folder)

Based on image apache/airflow:2.6.3 and add dependencies using pip install

```docker
FROM apache/airflow:latest-python3.9
apache-airflow-providers-smtp==1.2.0
```
> apache-airflow-providers-smtp==1.2.0 Requires-Python ~=3.8;

	
2. update docker-compose.yaml

comment image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.3} and uncomment build: .

```yaml
#image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.3}
build: .
```

3. build custom docker image

`docker compose build`

4. run custom image of  Airflow

`docker compose up`





# docker-compose.yaml

- services
`restart: always`

- Disable auto start container
`docker update --restart=no [container id]`

- volumes
`- ${AIRFLOW_PROJ_DIR:-.}/config/airflow.cfg:/opt/airflow/airflow.cfg`



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

1. event driven by new file (trade feed/ price feed)

2. generate reports and send emails

3. manage job dependencies 



# Enable OpenSSH Server in Win11 for SSHOperator

1. Settings, App, Optional features, New features, Install OpenSSH server
2. Services, OpenSSH server, Automatic Startup
3. Settings, Privacy and security, Windows Security, Firewall, Advance Settings
4. Inbound Rules, New rules, Port, TCP, port = 22


# Test connection in docker

`curl telnet://smtp-mail.outlook.com:587`


# Dockerfile

- Dockerfile is separated each command line by layer and cached. 

- shell form (processed by shell session)
`RUN npm install`

- exec form
`CMD ["npm", "start"]

- data is lost after container is stopped

- volume is used to persist data

- 1 process per container

- docker compose is used to run multiple containers at the same time


