# Workflow orchestration with Prefect

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Prefect](https://img.shields.io/badge/Prefect-3.1-060F11?style=flat&logo=prefect&logoColor=white&labelColor=060F11)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This GitHub project streamlines `Prefect Flows` to fetch NYC Taxi Tripdata CSV datasets from specified endpoints in app.yml and seamlessly sink them into Postgres and Google Cloud Storage.

**Note**: The `Prefect Orion` server is now called `Prefect Server`

## Tech Stack
- [Prefect](https://www.prefect.io/opensource/)
- [pandas](https://pandas.pydata.org/docs/user_guide/)
- [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Docker](https://docs.docker.com/get-docker/)

## Up and Running

### Developer Setup

**1.** Install the dependencies on `pyproject.toml`:
```shell
uv sync
```

**2.** Activate the virtualenv created by `uv`:
```shell
source .venv/bin/activate
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

**5.** Setup Prefect server for the flows:
```shell
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

### Prefect Flows

#### flows/web_csv_to_gcs.py:

Set the `GOOGLE_APPLICATION_CREDENTIALS` env variable.
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcs_credentials.json
```

Execute the flow with:
```shell
python flows/web_cs_to_gcs.py
```

#### flows/sqlalchemy_ingest.py:

Set the environment variables:
```shell
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DB=nyc_taxi
```

And then execute with:
```shell
python flows/sqlalchemy_ingest.py
```

## TODO:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Deploy Prefect Server / Agent on Docker
- [x] Code format/lint with Ruff
- [ ] Run Prefect flows on Docker
