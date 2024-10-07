# dbt and DuckDB for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.12_|_3.11_|_3.10-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.8-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![DuckDB](https://img.shields.io/badge/DuckDB-black?style=flat&logo=duckdb&logoColor=FEF000&labelColor=black)
![gcsfs](https://img.shields.io/badge/gcsfs-black?style=flat&logo=googlecloudstorage&logoColor=FEF000&labelColor=black)
![s3fs](https://img.shields.io/badge/s3fs-black?style=flat&logo=amazon-s3&logoColor=FEF000&labelColor=black)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-duckdb` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique. 

It also adds Data Reliability on top of that with PipeRider.

## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-duckdb](https://docs.getdbt.com/reference/warehouse-setups/duckdb-setup)
- [fsspec](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv with conda:
```shell
conda create -n dbt-duckdb python=3.12 -y
conda activate dbt-duckdb
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync --no-self
```

**3. (Optional)**  Install pre-commit:
```shell
brew install pre-commit
```

From root folder where `.pre-commit-config.yaml` is located, run:
```shell
pre-commit install
```

**4.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yml` as template)

4.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

4.2. Set the environment variables for `dbt-duckdb`:
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

4.3. If you're reading data from gcs, authenticate with:
```shell
gcloud auth login
```

4.4. Additionally, If you're reading data from s3, make sure to set `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY`:
```shell
export AWS_ACCESS_KEY=
export AWS_SECRET_ACCESS_KEY=
```

**5.** Install dbt dependencies and trigger the pipeline

5.1. Run `dbt deps` to install  dbt plugins
```shell
dbt deps
```

5.2. Run `dbt seed` to push/create the tables from the .csv seed files to the target schema
```shell
dbt seed
```

5.3. Run dbt run to trigger the dbt models to run
```shell
dbt build

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+
```

**6.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
dbt docs serve
```

Access the generated docs at:
```shell
open http://localhost:8080
```


## Containerization and Testing

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


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with DuckDB Adapter ([dbt-duckdb](https://github.com/duckdb/dbt-duckdb))
- [x] Configure dbt-duckdb with `fsspec` and read from [gcsfs](https://gcsfs.readthedocs.io/en/latest/api.html?highlight=GCSFileSystem#gcsfs.core.GCSFileSystem)
- [x] Configure dbt-duckdb with `fsspec` and read from [s3fs](https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem)
