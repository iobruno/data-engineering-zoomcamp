# Prefect Workflow Orchestration

This subproject is designed for `Prefect Flows` to fetch the CSV datasets for NYC Taxi Tripdata,
based on the endpoints provided on `app.yml` and sink them into:
- Postgres
- Google Cloud Storage


## Tech Stack
- Python 3.9 / 3.10 / 3.11
- pandas
- [Prefect](https://www.prefect.io/opensource/)
- [PDM](https://pdm-project.org/latest/#installation)
- [Ruff](https://github.com/astral-sh/ruff)
- Docker


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n prefect python=3.9 -y
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
export DATABASE_USERNAME=postgres && \
export DATABASE_PASSWORD=postgres && \
export DATABASE_HOST=localhost && \
export DATABASE_PORT=5433 && \
export DATABASE_NAME=nyc_taxi
```

```shell
python flows/sqlalchemy_ingest.py
```


## TODO:
- [x] Externalize configurations to config file (app.yml)
- [x] Handle dependency management with Poetry
- [x] Implement a python fmt with [yapf](https://github.com/google/yapf)