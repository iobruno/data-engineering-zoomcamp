# Prefect Workflow Orchestration

This subproject is designed to build a `Prefect Workflows` to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones based on the endpoints and persist them into three different sinks:
- Postgres
- GCP BigQuery
- Google Cloud Storage

## Tech Stack
- Python 3.9.+
- **Dataframe**: pandas, numpy
- **Workflow**: `prefect`
- **Virtualenv**: Conda
- **Dependency Management**: Poetry

## Up and Running

### Developer Setup

**Create and activate a virtualenv for Python 3.9 with conda**:
```bash
conda create -n de-zoomcamp python=3.9 -y
conda activate de-zoomcamp
```

**Install the dependencies on `pyproject.toml`**:
```bash
poetry install --no-root
```

**Start the Orion Server**:
```bash
prefect orion start
```

**Flow: flow_web_csv_dataset_to_csv.py**:

- Before running `flows/flow_web_csv_dataset_to_csv.py`, you should uncomment/add the lines under `datasets.green_trip_data` 
  and `datasets.yellow_trip_data` that contains the URL for the dataset you want to be on GCS
- The source of the dataset must be in `.csv` or `.csv.gz`
- The target on GCS will always be as `.parquet.gz`

```bash
python flows/flow_web_csv_dataset_to_csv.py
```

**Flow: flow_gcs_to_bq.py**:
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


```bash
python flows/flow_gcs_to_bq.py
```

## TODO:
- [x] Externalize configurations to config file (app.yml)
- [x] Handle dependency management with Poetry
- [x] Implement a python fmt with [yapf](https://github.com/google/yapf)
