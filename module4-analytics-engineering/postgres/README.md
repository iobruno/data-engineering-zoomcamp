# dbt and PostgreSQL for Analytics

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)](https://hub.docker.com/_/postgres)
[![dbt](https://img.shields.io/badge/dbt--postgres-1.9-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-postgres` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique.

**NOTE**: This is NOT meant for production at scale, but rather for educational purposes. Consider using `BigQuery`, `Snowflake`, `StarRocks`, `ClickHouse`, `Databricks` or `RedShift` instead.


## 🛠️ Getting Started

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

**3.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yaml` as template)

3.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

3.2. Set the environment variables for `dbt-postgres`:
```shell
export DBT_POSTGRES_HOST=localhost
export DBT_POSTGRES_PORT=5432
export DBT_POSTGRES_DATABASE=nyc_taxi
export DBT_POSTGRES_SOURCE_SCHEMA=public
export DBT_POSTGRES_TARGET_SCHEMA=nyc_tlc_record_data
export DBT_POSTGRES_USER=postgres
export DBT_POSTGRES_PASSWORD=postgres
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
dbt build --target [prod|dev]

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging --target [prod|dev]

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+ --target [prod|dev]
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


## 🐳 Containerization

**1.** Build the Docker Image with:
```shell
docker build -t dbt-postgres:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e DBT_POSTGRES_HOST=host.docker.internal \
  -e DBT_POSTGRES_DATABASE=nyc_taxi \
  -e DBT_POSTGRES_SOURCE_SCHEMA=public \
  -e DBT_POSTGRES_TARGET_SCHEMA=nyc_tlc_record_data \
  -e DBT_POSTGRES_USER=postgres \
  -e DBT_POSTGRES_PASSWORD=postgres \
  --name dbt-postgres \
  dbt-postgres
```


## 📋 TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with PostgreSQL Adapter ([dbt-postgres](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [x] Add dbt macro to configure target schemas dinamically
- [x] Run `dbt-core` in Docker
