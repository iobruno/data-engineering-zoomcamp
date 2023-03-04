# Prefect Workflow Orchestration

This subproject is designed to build a `Prefect Workflows` to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones based on the endpoints and persist them into three different sinks:
- Postgres
- GCP BigQuery
- Google Cloud Storage

## Tech Stack
- Python 3.9 / 3.10
- pandas, numpy
- [Prefect](https://www.prefect.io/opensource/)
- [Poetry](https://python-poetry.org/docs/)

## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n de-zoomcamp python=3.9 -y
conda activate de-zoomcamp
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

**4.** Start the Orion Server:
```shell
prefect orion start
```

### Prefect Flows

**flows/web_csv_dataset_to_csv.py**:

- Before running `flows/web_csv_dataset_to_csv.py`, you should uncomment/add the lines under `datasets.green_trip_data`
  and `datasets.yellow_trip_data` that contains the URL for the dataset you want to be on GCS
- The source of the dataset must be in `.csv` or `.csv.gz`
- The target on GCS will always be as `.parquet.gz`

```shell
python flows/web_csv_dataset_to_csv.py
```

**flows/gcs_to_bq.py**:
- Before running `flows/flow_gcs_to_bq.py`, you should ADD entries **as a list**, under `etl.gcs_to_bigquery.yellow` and/or
  `etl.gcs_to_bigquery.green`, using the format
- The entries MUST be formatted as: `YYYY-MM`
- The config below means, the flow will attempt to search GCS for `yellow_taxi_tripdata`, for the year-months: `2019-03`
  and `2019-02`, and load them up into BigQuery.

```yaml
etl:
  gcs_to_bigquery:
    yellow:
      - "2019-03"
      - "2019-02"
```

```shell
python flows/gcs_to_bq.py
```

## TODO:
- [x] Externalize configurations to config file (app.yml)
- [x] Handle dependency management with Poetry
- [x] Implement a python fmt with [yapf](https://github.com/google/yapf)
