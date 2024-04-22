### 1. change directory to project 05-creating-and-scheduling-data-pipelines:
```sh
cd 05-creating-and-scheduling-data-pipelines/
```

### 2. prepare environment workspace 
(https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

```sh
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

docker-compose.yaml Input # (stop working code)

`line 56` 

56 AIRFLOW__CORE__EXECUTOR: CeleryExecutor 

`Adding line 57 working replace to line 56`

57 AIRFLOW__CORE__EXECUTOR: LocalExecutor

`line 59-60` 

59 AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow

60 AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

`line 81-82` 

81 redis:

82 condition: service_healthy

`line 102-112` from

102 redis:

112 restart: always

`line 146-182` from

146 airflow-worker:

182 condition: service_completed_successfully

`line 261-263`

261 You can enable flower by adding "--profile flower" option e.g. docker-compose --profile flower up

262 or by explicitly targeted on the command line e.g. docker-compose up flower.

263 See: https://docs.docker.com/compose/profiles/


### Running Docker

```sh
docker-compose up
```

### 3. Airflow
Airflow UI port 8080 (localhost:8080)

User & Password : airflow (by default line 241-242)

### Shutdown environment workspace:
```sh
$ docker-compose down
```





