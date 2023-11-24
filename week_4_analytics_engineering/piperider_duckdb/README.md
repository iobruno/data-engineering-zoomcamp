# Data Observability with PipeRider, dbt, and DuckDB Project:

![Python](https://img.shields.io/badge/Python-3.9%20|%203.10%20|%203.11-3776AB.svg?style=flat&logo=python&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Enhance data observability with dbt, DuckDB, and PipeRider. This project focuses on building a dbt model on DuckDB and integrating PipeRider pipelines for robust data observability.


## Tech Stack
- [dbt-core](https://github.com/dbt-labs/dbt-core)
- [dbt-duckdb](https://docs.getdbt.com/reference/warehouse-setups/duckdb-setup)
- [PipeRider](https://github.com/InfuseAI/piperider)
- [PDM](https://pdm-project.org/latest/#installation)
- [Ruff](https://github.com/astral-sh/ruff)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n dbt-duckdb python=3.11 -y
conda activate dbt-duckdb
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

**5.** Run `dbt deps` and `dbt build`:
```shell
dbt deps
dbt build
```

**5.** Initialize the PipeRider setup and run it for the first time:
```shell
piperider init 
piperider run
```


## TODO:
- [x] Bootstrap dbt with DuckDB Adapter for NY Tripdata
- [x] Integrate with PipeRider and generate reports
- [x] Modify the dbt models, generate a new report and compare
- [x] Utilize the comparison on a [GitHub Pull Request](https://github.com/iobruno/data-engineering-zoomcamp/pull/2)
- [x] Replace Poetry with PDM
- [ ] Set up a CI Pipeline with GitHub Actions