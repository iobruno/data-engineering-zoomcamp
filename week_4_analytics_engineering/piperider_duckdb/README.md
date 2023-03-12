# dbt and PipeRider for Data Observability

This subproject is designed to build a `dbt` model on top of DuckDB, and have some PipeRider pipelines for Data Observability


## Tech Stack
- Python 3.9 / 3.10
- DuckDB
- PipeRider
- [dbt-duckdb](https://docs.getdbt.com/reference/warehouse-setups/duckdb-setup)
- [Poetry](https://python-poetry.org/docs/)


## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n dbt-duckdb python=3.10 -y
conda activate dbt-duckdb
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
poetry install --no-root
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

## Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## TODO:
- [ ] Bootstrap dbt with DuckDB Adapter
- [ ] Integrate with PipeRider
