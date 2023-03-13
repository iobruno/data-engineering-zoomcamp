# dbt and PipeRider for Data Observability

This subproject is designed to build a `dbt` model on top of DuckDB, and have PipeRider for profiling our models, and generate reports for better Observability.

![workshop-piperider-workflow](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/workshop_piperider_workflow.png)


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

T.B.D.

## Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## TODO:
- [x] Bootstrap dbt with DuckDB Adapter for NY Tripdata
- [x] Integrate with PipeRider and generate reports
- [x] Modify the dbt models, generate a new report and compare
- [x] Utilize the comparison on a [GitHub Pull Request](https://github.com/iobruno/data-engineering-zoomcamp/pull/2)
- [ ] Set up a CI Pipeline with GitHub Actions
