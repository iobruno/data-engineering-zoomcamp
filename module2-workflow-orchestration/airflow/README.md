# Airflow Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Airflow](https://img.shields.io/badge/Airflow-2.7-3772FF?style=flat&logo=apacheairflow&logoColor=white&labelColor=3772FF)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This setups the infrastructure for Airflow, in Docker, as close as possible to a deploy in a Kubernetes/Helm environment: having containers for the `airflow-scheduler`, `airflow-web`, `airflow-triggerer`, and `airflow-worker` (the CeleryExecutor)


## Tech Stack
- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- [pandas](https://pandas.pydata.org/docs/user_guide/)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup (Docker)

**1.** Start setting up the infrastructure in Docker with:

**Airflow with CeleryExecutor**:
```shell
docker compose -f docker-compose.celery.yml up -d
```

**Airflow with LocalExecutor**:
```shell
docker compose -f docker-compose.local.yml up -d
```


**2.** Airflow WebUI can be accessed at:

```shell
open http://localhost:8080
```

**3.** Airflow DAGs

To deploy Airflow DAGs, just move them inside the [dags](dags/) folder and Airflow should pick it up soon enough


## TODO:
- [ ] PEP-517: Packaging and dependency management with PDM
- [ ] Code format/lint with Ruff
- [ ]  Run Airflow DAGs on Docker
- [ ] Complete [Astronomer Academy's Airflow 101](https://academy.astronomer.io/path/airflow-101)
- [ ] Deploy [Airflow to Kubernetes with Helm](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [ ] Run/Deploy [Airflow DAGs on Kubernetes with KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)