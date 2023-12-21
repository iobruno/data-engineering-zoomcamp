# dbt and ClickHouse for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dbt](https://img.shields.io/badge/dbt-1.7-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)
![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project focuses on creating dbt models using the NY Taxi Tripdata Datasets in ClickHouse.


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-clickhouse](https://docs.getdbt.com/docs/core/connect-data-platform/clickhouse-setup)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 / 3.11 with conda:
```shell
conda create -n dbt-clickhouse python=3.11 -y
conda activate dbt-clickhouse
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

4.2. Configure the gcp `host`, `port`, `dbname`, `schema`, `user` and `pass` (password) to where BigQuery should create its tables/views in (on `profiles.yml`)

```yaml
  host: localhost
  port: 5433
  dbname: REPLACE_ME
  user: REPLACE_ME
  pass: REPLACE_ME
  schema: stg_nyc_trip_record_data
  threads: 4
```

4.3. On [models/staging/schema.yml](models/staging/schema.yml), make sure to update the `database`, `schema`, and `tables` that the staging models fetch the data from
```shell
  - name: pg-raw-nyc-trip-record
    database: nyc_taxi
    schema: raw_nyc_trip_record_data
    tables:
      - name: ntl_green_taxi
      - name: ntl_yellow_taxi
```

4.4. Update the `profile` to used by this project on `dbt_project.yml`

Make sure to point to an existing profile name set on profiles.yaml. In this case:
```yaml
profile: 'postgres-clickhouse'
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


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Bootstrap dbt with PostgreSQL Adapter ([dbt-postgres](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [ ] Run `dbt-core` in Docker