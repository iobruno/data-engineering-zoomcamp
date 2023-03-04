# dbt for Analytics Engineering 

This subproject is designed to build a `dbt` models from the `NY Taxi Tripdata Datasets` on BigQuery, 
and Dashboards on `Looker Studio` (formerly: `Google Data Studio`) for Data Visualizations 

## Tech Stack
- [dbt-bigquery](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
- BigQuery 
- Looker Studio 

## Up and Running

### Developer Setup

**1.** Install **dbt**, with the associated adapter for your Datasource 
```shell
brew update
brew tap dbt-labs/dbt
brew install dbt-bigquery
```

**2.** Run `dbt run` to trigger the dbt models to run:
```shell
dbt run
```

**3.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
```
```shell
dbt docs serve
```

**4.** Access the generated docs on a web browser at the URL:
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
