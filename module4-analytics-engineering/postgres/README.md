# dbt and PostgreSQL for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.7-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project focuses on creating dbt models using the NY Taxi Tripdata Datasets in PostgreSQL. 

**IMPORTANT NOTE**: This is **not** meant for production use at scale, but rather for educational purposes only. Consider using `RedShift`, `BigQuery`, `Snowflake` or `Databricks` instead. If those options are too costy, or if you need something for on-premises deploy, consider `Clickhouse` instead.


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-postgres](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 / 3.11 with conda:
```shell
conda create -n dbt-postgres python=3.11 -y
conda activate dbt-postgres
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
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

4.2. Set the environment variables for `dbt-postgres`:

```shell
export DBT_POSTGRES_HOST=localhost \
export DBT_POSTGRES_PORT=5433 \
export DBT_POSTGRES_DATABASE=nyc_taxi \
export DBT_POSTGRES_SOURCE_SCHEMA=public \
export DBT_POSTGRES_TARGET_SCHEMA=nyc_trip_record_data \
export DBT_POSTGRES_USER=postgres \
export DBT_POSTGRES_PASSWORD=postgres
```

4.3. On [models/staging/schema.yml](models/staging/schema.yml), make sure to update the `tables` names where the staging models fetch the data from
```shell
  - name: pg-raw-nyc-trip_record
    database: "{{ env_var('DBT_POSTGRES_DATABASE') }}"
    schema: "{{ 'raw_' ~ env_var('DBT_POSTGRES_SCHEMA') }}"
    tables:
      - name: ntl_green_taxi
      - name: ntl_yellow_taxi
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
```
```shell
dbt docs serve
```

**7.** Access the generated docs on a web browser at the URL:
```shell
open http://localhost:8080
```


## Containerization and Testing

**1.** Build the Docker Image with:

```shell
docker build -t dbt_postgres:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run \
  -e DBT_POSTGRES_HOST=postgres \
  -e DBT_POSTGRES_DATABASE=nyc_taxi \
  -e DBT_POSTGRES_SOURCE_SCHEMA=public \
  -e DBT_POSTGRES_TARGET_SCHEMA=nyc_trip_record_data \
  -e DBT_POSTGRES_USER=postgres \
  -e DBT_POSTGRES_PASSWORD=postgres \
  --network dbt_analytics \
  --name dbt_postgres \
  dbt_postgres
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with PostgreSQL Adapter ([dbt-postgres](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [x] Add dbt macro to configure target schemas dinamically
- [x] Run `dbt-core` in Docker
- [ ] Add migrations to initialize PostgreSQL with some data