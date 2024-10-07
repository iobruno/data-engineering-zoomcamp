# dbt and ClickHouse for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.12_|_3.11_|_3.10-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.8-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-clickhouse` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique.


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-clickhouse](https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv with conda:
```shell
conda create -n dbt-clickhouse python=3.12 -y
conda activate dbt-clickhouse
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

**4.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yaml` as template)

4.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

4.2. Set the environment variables for `dbt-clickhouse`:
```shell
export DBT_CLICKHOUSE_HOST=localhost
export DBT_CLICKHOUSE_PORT=8123
export DBT_CLICKHOUSE_FQDN_NYC_TAXI=fqdb_nyc_taxi
export DBT_CLICKHOUSE_TARGET_DATABASE=nyc_tlc_record_data
export DBT_CLICKHOUSE_USER=clickhouse
export DBT_CLICKHOUSE_PASSWORD=clickhouse
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
dbt build --target [prod|dev]

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging --target [prod|dev]

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+ --target [prod|dev]
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


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with ClickHouse Adapter ([dbt-clickhouse](https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [x] Run `dbt-core` in Docker
- [x] Build at least one dbt staging_model based on Federated Queries on PostgreSQL