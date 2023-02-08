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

## TODO:
- [x] Externalize configurations to config file (app.yml)
- [x] Handle dependency management with Poetry
- [x] Implement a python fmt with [yapf](https://github.com/google/yapf)
