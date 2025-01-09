# dbt and BigQuery for Analytics

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![dbt](https://img.shields.io/badge/dbt--bigquery-1.9-262A38?style=flat&logo=dbt&logoColor=FF6849&labelColor=262A38)](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project is meant for experimenting with `dbt` and the `dbt-bigquery` adapter for Analytics,
using [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) dataset as the datasource, with Kimball dimensional modeling technique.


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

**3.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yaml` as template)

3.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

3.2. Set the environment variables for `dbt-bigquery`:
```shell
export DBT_BIGQUERY_PROJECT=iobruno-gcp-labs
export DBT_BIGQUERY_SOURCE_DATASET=raw_nyc_tlc_trip_data
export DBT_BIGQUERY_TARGET_DATASET=nyc_tlc_trip_data
export DBT_BIGQUERY_DATASET_LOCATION=us-central1
```

3.3. Since we're doing `oauth` authentication for our Development env, run:
```shell
gcloud auth login
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
docker build -t dbt-bigquery:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e DBT_BIGQUERY_PROJECT=iobruno-gcp-labs \
  -e DBT_BIGQUERY_SOURCE_DATASET=raw_nyc_tlc_trip_data \
  -e DBT_BIGQUERY_TARGET_DATASET=nyc_tlc_trip_data \
  -e DBT_BIGQUERY_DATASET_LOCATION=us-central1 \
  -v /PATH/TO/YOUR/gcp_credentials.json:/secrets/gcp_credentials.json \
  --name dbt-bigquery \
  dbt-bigquery
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with BigQuery Adapter ([dbt-bigquery](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup))
- [x] Generate and serve docs and Data Lineage Graphs locally
- [x] Add dbt macro to configure target schemas dinamically
- [x] Run `dbt-core` in Docker
- [ ] Complete dbt Labs Learning Path for `dbt-core`
  - [ ] [dbt Fundamentals](https://courses.getdbt.com/courses/fundamentals)
  - [ ] [Jinja, Macros, Packages](https://courses.getdbt.com/courses/jinja-macros-packages)
  - [ ] [Advanced Materializations](https://courses.getdbt.com/courses/advanced-materializations)
  - [ ] [Refactoring SQL for Modularity](https://courses.getdbt.com/courses/refactoring-sql-for-modularity)
  - [ ] [Analyses and Seeds](https://courses.getdbt.com/courses/analyses-seeds)
  - [ ] [Advanced Testing](https://courses.getdbt.com/courses/advanced-testing)
- [ ] Implement Data Quality metrics it with [dbt-expectations](https://github.com/calogica/dbt-expectations)
- [ ] Implement Data Observability with [elementary-data](https://github.com/elementary-data/elementary)
