# dbt and ClickHouse for Analytics

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)](https://clickhouse.com/docs/en/install)
[![dbt](https://img.shields.io/badge/dbt--clickhouse-1.8-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)](https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-clickhouse` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique.


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

3.2. Set the environment variables for `dbt-clickhouse`:
```shell
export DBT_CLICKHOUSE_HOST=localhost
export DBT_CLICKHOUSE_PORT=8123
export DBT_CLICKHOUSE_FQDN_NYC_TAXI=fqdb_nyc_taxi
export DBT_CLICKHOUSE_TARGET_DATABASE=nyc_tlc_record_data
export DBT_CLICKHOUSE_USER=clickhouse
export DBT_CLICKHOUSE_PASSWORD=clickhouse
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

**1.** With your instance of Clickhouse and Postgres up, connect to ClickHouse and run:
```sql
CREATE DATABASE fqdb_nyc_taxi
ENGINE = PostgreSQL('host.docker.internal:5432', 'nyc_taxi', 'postgres', 'postgres', 'public', 0);
```

**2.** Build the Docker Image with:
```shell
docker build -t dbt-clickhouse:latest . --no-cache
```

**3.** Fire up the container with it:
```shell
docker run -d --rm \
  -e DBT_CLICKHOUSE_HOST=host.docker.internal \
  -e DBT_CLICKHOUSE_FQDN_NYC_TAXI=fqdb_nyc_taxi \
  -e DBT_CLICKHOUSE_TARGET_DATABASE=nyc_tlc_record_data \
  -e DBT_CLICKHOUSE_USER=clickhouse \
  -e DBT_CLICKHOUSE_PASSWORD=clickhouse \
  --name dbt-clickhouse \
  dbt-clickhouse
```

## 📋 TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with ClickHouse Adapter ([dbt-clickhouse](https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [x] Run `dbt-core` in Docker
- [x] Build at least one dbt staging_model based on Federated Queries on PostgreSQL
