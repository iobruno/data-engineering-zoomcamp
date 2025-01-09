# dbt and DuckDB for Analytics

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![DuckDB](https://img.shields.io/badge/DuckDB-black?style=flat&logo=duckdb&logoColor=FEF000&labelColor=black)](https://duckdb.org/docs/)
[![gcsfs](https://img.shields.io/badge/gcsfs-black?style=flat&logo=googlecloudstorage&logoColor=FEF000&labelColor=black)](https://gcsfs.readthedocs.io/en/latest/)
[![s3fs](https://img.shields.io/badge/s3fs-black?style=flat&logo=amazon-s3&logoColor=FEF000&labelColor=black)](https://s3fs.readthedocs.io/en/latest/)
[![dbt](https://img.shields.io/badge/dbt--duckdb-1.9-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)](https://docs.getdbt.com/reference/warehouse-setups/duckdb-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-duckdb` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique. 

It also adds Data Reliability on top of that with PipeRider.


## Getting Started

**1.** Install dependencies from pyproject.toml and activate the created virtualenv:
```shell
uv sync && source .venv/bin/activate
```

**2.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**3.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yml` as template)

3.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

3.2. Set the environment variables for `dbt-duckdb`:
```shell
export DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/"
export DBT_DUCKDB_TARGET_PATH=~/.duckdb/dbt.duckdb
```

Optionally, you can also set the DuckDB schemas where the dbt staging & core models should land on:
```shell
# Schema for the dim_ and fct_ models; it defaults to 'main', when not set
export DBT_DUCKDB_TARGET_SCHEMA=analytics

# Schema for the stg_ models; it defaults to 'main', when not set
export DBT_DUCKDB_STAGING_SCHEMA=stg_analytics
```

3.3. If you're reading data from gcs, authenticate with:
```shell
gcloud auth login
```

3.4. Additionally, If you're reading data from s3, make sure to set `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY`:
```shell
export AWS_ACCESS_KEY=
export AWS_SECRET_ACCESS_KEY=
```

**4.** Install dbt dependencies and trigger the pipeline

4.1. Run `dbt deps` to install  dbt plugins
```shell
dbt deps
```

4.2. Run `dbt seed` to push/create the tables from the .csv seed files to the target schema
```shell
dbt seed
```

4.3. Run dbt run to trigger the dbt models to run
```shell
dbt build

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+
```

**5.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
dbt docs serve
```

Access the generated docs at:
```shell
open http://localhost:8080
```


## Containerization

**1.** Build the Docker Image with:
```shell
docker build -t dbt-duckdb:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/" \
  -e DBT_DUCKDB_TARGET_PATH=/duckdb/dbt.duckdb \
  -e DBT_DUCKDB_TARGET_SCHEMA=analytics \
  -v ~/.duckdb:/duckdb \
  -v PATH/TO/YOUR/gcp_credentials.json:/secrets/gcp_credentials.json \
  --name dbt-duckdb \
  dbt-duckdb
```

Note: If the container suddenly gets killed, it means it has run out-of-ram to process the full workload. Increase the amount of available RAM a container can use (on Docker settings).


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with DuckDB Adapter ([dbt-duckdb](https://github.com/duckdb/dbt-duckdb))
- [x] Configure dbt-duckdb with `fsspec` and read from [gcsfs](https://gcsfs.readthedocs.io/en/latest/api.html?highlight=GCSFileSystem#gcsfs.core.GCSFileSystem)
- [x] Configure dbt-duckdb with `fsspec` and read from [s3fs](https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem)
