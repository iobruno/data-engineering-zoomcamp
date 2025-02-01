# dltHub: data load tool

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![dltHub](https://img.shields.io/badge/dltHub-1.5-59C1D5?style=flat&logo=pandas&logoColor=59C1D5&labelColor=191A37)](https://dlthub.com/)
[![Polars](https://img.shields.io/badge/polars-24292E?style=flat&logo=polars&logoColor=CC792B&labelColor=24292E)](https://docs.pola.rs/)
[![DuckDB](https://img.shields.io/badge/DuckDB-0D0D0D?style=flat&logo=duckdb&logoColor=FEF000&labelColor=0D0D0D)](https://duckdb.org/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This is meant for experimenting with [data load tool (dlt)](https://dlthub.com/) for fetching data from APIs and persiting it to a local DuckDB, Google CloudStorage, and BigQuery.


## Getting Started

**1.** Create and activate a virtualenv for Python 3.11 with conda:
```shell
conda create -n dlt python=3.11 -y
conda activate dlt
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

**4.** Run the dlt pipeline
```shell
T.B.D.
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Code format/lint with Ruff
- [ ] Extract data from Web APIs with dlt
