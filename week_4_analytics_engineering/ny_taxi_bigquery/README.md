# dbt for Analytics Engineering

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776AB.svg?style=flat&logo=python&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This project focuses on creating dbt models using the NY Taxi Tripdata Datasets in BigQuery. Additionally, it involves developing Dashboards in `Looker Studio` (formerly known as `Google Data Studio`) for data visualizations


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-bigquery](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
- [PDM](https://pdm-project.org/latest/#installation)
- [Ruff](https://github.com/astral-sh/ruff)
- Looker Studio


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n dbt-bigquery python=3.11 -y
conda activate dbt-bigquery
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**5.** Run `dbt deps` to install dbt plugins
```shell
dbt deps
```

**5.** Run `dbt run` to trigger the dbt models to run:
```shell
dbt run
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
- [x] Bootstrap dbt with BigQuery Adapter
- [x] Generate and serve docs and Data Lineage Graphs locally
- [ ] Complete dbt Labs Learning Path for `dbt-core`
  - [ ] [dbt Fundamentals](https://courses.getdbt.com/courses/fundamentals)
  - [ ] [Jinja, Macros, Packages](https://courses.getdbt.com/courses/jinja-macros-packages)
  - [ ] [Advanced Materializations](https://courses.getdbt.com/courses/advanced-materializations)
  - [ ] [Refactoring SQL for Modularity](https://courses.getdbt.com/courses/refactoring-sql-for-modularity)
  - [ ] [Analyses and Seeds](https://courses.getdbt.com/courses/analyses-seeds)
  - [ ] [Advanced Testing](https://courses.getdbt.com/courses/advanced-testing)
- [ ] Implement Data Quality metrics it with [dbt-expectations](https://github.com/calogica/dbt-expectations)
- [ ] Implement Data Observability with [elementary-data](https://github.com/elementary-data/elementary)