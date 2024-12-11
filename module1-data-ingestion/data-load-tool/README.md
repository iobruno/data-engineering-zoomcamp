# data load tool (dlt)

![Python](https://img.shields.io/badge/Python-3.12_|_3.11_|_3.10-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![dltHub](https://img.shields.io/badge/dltHub-59C1D5?style=flat&logo=pandas&logoColor=C6D300&labelColor=59C1D5)
![DuckDB](https://img.shields.io/badge/DuckDB-black?style=flat&logo=duckdb&logoColor=FEF000&labelColor=black)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This is meant for experimenting with [data load tool (dlt)](https://dlthub.com/) for fetching data Web APIs and persiting it to a local DB

## Tech Stack
- [data load tool (dlt)](https://dlthub.com/)
- [DuckDB](https://duckdb.org/)
- [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Docker](https://docs.docker.com/get-docker/)

## Up and Running

### Developer Setup

**1.** Install the dependencies on `pyproject.toml`:
```shell
uv sync
```

**2.** Activate the virtualenv created by `uv`:
```shell
source .venv/bin/activate
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**4.** Run the dlt pipeline
- T.B.D.

## TODO:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Code format/lint with Ruff
- [ ] Extract data from Web APIs with dlt
