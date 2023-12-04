# Airflow Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Airflow](https://img.shields.io/badge/Airflow-2.7-3772FF?style=flat&logo=apacheairflow&logoColor=white&labelColor=3772FF)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

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
