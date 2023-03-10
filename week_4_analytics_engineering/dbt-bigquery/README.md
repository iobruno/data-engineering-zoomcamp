# dbt for Analytics Engineering

This subproject is designed to build a `dbt` models from the `NY Taxi Tripdata Datasets` on BigQuery,
and Dashboards on `Looker Studio` (formerly: `Google Data Studio`) for Data Visualizations

## Tech Stack
- Python 3.9 / 3.10
- BigQuery
- [dbt-bigquery](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
- Looker Studio
- [Poetry](https://python-poetry.org/docs/)

## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.9 with conda:
```shell
conda create -n de-zoomcamp python=3.9 -y
conda activate de-zoomcamp
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

**4.** Run `dbt run` to trigger the dbt models to run:
```shell
dbt run
```

**5.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
```
```shell
dbt docs serve
```

**6.** Access the generated docs on a web browser at the URL:
```shell
http://localhost:8080
```

## Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## TODO:
- [x] Getting Started with dbt
- [x] Generate and serve docs and Data Lineage Graphs locally
- [ ] Orchestrate the dbt execution with Airflow/Prefect
- [ ] Integrate it with a Data Quality/Observability
