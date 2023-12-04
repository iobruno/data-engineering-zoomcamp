# Mage.ai Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Mage.ai](https://img.shields.io/badge/Mage.ai-0.9-111113?style=flat&logoColor=white&labelColor=111113)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This GitHub project streamlines `Mage pipelines` to fetch NYC Taxi Tripdata CSV datasets from specified endpoints in app.yml and seamlessly sink them into Postgres and Google Cloud Storage.


## Tech Stack
- [Mage.ai](https://docs.mage.ai/getting-started/setup)
- pandas
- [PDM](https://pdm-project.org/latest/#installation)
- [Ruff](https://github.com/astral-sh/ruff)
- Docker


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n mage python=3.11 -y
conda activate mage
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
```

**3.** Start Mage Web UI:
```shell
mage start
```


**4.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```


### Mage pipelines

- T.B.D.


## TODO:
- [ ] PEP-517: Packaging and dependency management with PDM
- [ ] Code format/lint with Ruff
- [ ] Run Mage pipelines on Docker
- [ ] Deploy [Mage to Kubernetes with Helm](https://docs.mage.ai/production/deploying-to-cloud/using-helm)
- [ ] Run/Deploy Mage pipelines on Kubernetes
