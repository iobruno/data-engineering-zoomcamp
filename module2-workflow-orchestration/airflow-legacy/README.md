# Airflow Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.8_|_3.9-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Airflow](https://img.shields.io/badge/Airflow-1.10.15-00C9D6?style=flat&logo=apacheairflow&logoColor=white&labelColor=007A87)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


Do **NOT** use this for new projects. Instead refer to [Airflow 2.x](../airflow/)

Infrastructure setup for Airflow 1.x in Docker, optimized for native execution on Apple Silicon (arm64). Designed specifically for handling legacy Airflow environments, such as migrations from Airflow 1.x DAGs to Airflow 2.x.


## Tech Stack
- [Airflow 1.10.15](https://airflow.apache.org/docs/apache-airflow/1.10.15/)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup (Docker)

**1.** Start setting up the infrastructure in Docker with:
```shell
docker compose up -d
```

**2.** Airflow WebUI can be accessed at:

```shell
open http://localhost:8080
```

**3.** Airflow DAGs

To deploy Airflow DAGs, just move them inside the [dags](dags/) folder and Airflow should pick it up soon enough


## TODO:
- [x] Airflow infrastructure in Docker
- [x] Run Airflow DAGs on Docker
