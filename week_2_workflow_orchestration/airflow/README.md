# Airflow Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776AB.svg?style=flat&logo=python&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)

This GitHub project streamlines `Airflow DAGs` to fetch NYC Taxi Tripdata CSV datasets from specified endpoints in app.yml and seamlessly sink them into Postgres and Google Cloud Storage.


## Tech Stack
- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- pandas
- [PDM](https://pdm-project.org/latest/#installation)
- [Ruff](https://github.com/astral-sh/ruff)
- Docker


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n airflow python=3.11 -y
conda activate airflow
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```


### Airflow DAGs

- T.B.D.


## TODO:
- [ ] PEP-517: Packaging and dependency management with PDM
- [ ] Code format/lint with Ruff
- [ ] Run Airflow DAGs on Docker
- [ ] Complete [Astronomer Academy's Airflow 101](https://academy.astronomer.io/path/airflow-101)
- [ ] Deploy [Airflow to Kubernetes with Helm](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [ ] Run/Deploy [Airflow DAGs on Kubernetes with KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
