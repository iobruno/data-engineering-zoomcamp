# Prefect Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Prefect](https://img.shields.io/badge/Prefect-2.14-060F11?style=flat&logo=prefect&logoColor=white&labelColor=060F11)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This GitHub project streamlines `Prefect Flows` to fetch NYC Taxi Tripdata CSV datasets from specified endpoints in app.yml and seamlessly sink them into Postgres and Google Cloud Storage.

*Note*: The `Prefect Orion` server is now called `Prefect Server`

## Tech Stack
- [Prefect](https://www.prefect.io/opensource/)
- [pandas](https://pandas.pydata.org/docs/user_guide/)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n prefect python=3.11 -y
conda activate prefect
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

**4.** Start the Prefect Server:
```shell
prefect server start
```

### Prefect Flows

**flows/web_csv_to_gcs.py**:

For the very first run:
- You need to set `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
  That will enable the flow to automatically create the `GcsBucket` and `GcpCredentials` Prefect Blocks

- Before running `flows/web_csv_to_gcs.py`, you should comment out/uncomment the endpoints in `app.yml`
  under `datasets.green`, `datasets.yelow`, and `datasets.fhv`

```shell
python flows/web_cs_to_gcs.py
```

**flows/sqlalchemy_ingest.py**:

For the very first run:
- Make sure to set the environment variables: `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USERNAME`, and `DATABASE_PASSWORD`,
- Also, configure the database name it should connect to on `app.yml` under the key: `prefect_block.sqlalchemy.ny_taxi.database`
```shell
export DATABASE_USERNAME=postgres \
export DATABASE_PASSWORD=postgres \
export DATABASE_HOST=localhost \
export DATABASE_PORT=5433 \
export DATABASE_NAME=nyc_taxi
```

```shell
python flows/sqlalchemy_ingest.py
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Code format/lint with Ruff
- [ ] Run Prefect flows on Docker
