# Mage.ai Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776AB.svg?style=flat&logo=python&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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
- [ ] Implement Pipelines with Mage on Docker
- [ ] PEP-517: Packaging and dependency management with PDM
- [ ] Code format/lint with Ruff
