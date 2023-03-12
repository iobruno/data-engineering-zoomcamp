# Airflow: Postgres Ingest

This subproject is designed to build `Airflow DAGs` to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones based on the endpoints and persist them into three different sinks:
- Postgres
- GCP BigQuery
- Google Cloud Storage

## Tech Stack
- Python 3.9 / 3.10
- pandas, numpy
- [Airflow](https://airflow.apache.org/)
- [Poetry](https://python-poetry.org/docs/)

## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n airflow python=3.10 -y
conda activate airflow
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
poetry install --no-root
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

## TODO:
- T.B.D.
