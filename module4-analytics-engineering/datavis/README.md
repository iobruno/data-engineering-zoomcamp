# Data Visualzation with Superset and Metabase

![Superset](https://img.shields.io/badge/Superset-0A2933?style=flat&logo=apache&logoColor=F8FDFF&labelColor=0A2933)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=flat&logo=metabase&logoColor=white&labelColor=65A9E7)
![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)
![Redshift](https://img.shields.io/badge/AWS_Redshift-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)
![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Tech Stack
- [Apache Superset](https://superset.apache.org/)
- [Metabase Open Source](https://www.metabase.com/start/oss/)
- [Docker](https://docs.docker.com/get-docker/)


## Up & Running

### Superset

**0.** (Optional) Pre-loaded examples (demo charts/dashboards):

Superset can be bootstrapped withexample charts and dashboards. In order to enable that, set:
```shell
export SUPERSET_LOAD_EXAMPLES=yes
```

Make sure to: `unset SUPERSET_LOAD_EXAMPLES` or `export SUPERSET_LOAD_EXAMPLES=no`  after the **first run** of `superset-init` is completed successfully, as `load_examples` alone can take a few minutes.

**1.** Spin up Apache Superset infrastructure with:
```shell
docker compose -f compose.superset.yaml up -d
```

**2.** Additional database drivers:

Superset supports PostgreSQL, MySQL and out-of-the-box. To enable additional data sources, include the respective `SQLAlchemy` driver as a dependency in [requirements-local.txt](./superset/requirements-local.txt). 

A complete list of supported data sources can be found [here](https://superset.apache.org/docs/databases/installing-database-drivers/).

```python
sqlalchemy-bigquery==1.11.0
sqlalchemy-redshift==0.8.14
clickhouse-connect==0.7.16
```

**3.** After the `superset-app` container is in a healthy state, you can acccess Superset at:
```shell
open http://localhost:8088/
```


### Metabase

**1.** Spin up Metabase infrastructure with:

```shell
docker compose -f compose.metabase.yaml up -d
```

**2.** Additional database drivers:

Metabase supports a wide-variety of data sources out-of-the-box (BigQuery, RedShift, Snowflake, Spark SQL, Druid, PostgreSQL, MySQL, among others). The complete list of supported data sources can be found [here](https://www.metabase.com/data_sources/).

For Partners Data Sources and Community Data Source connectors, such as `ClickHouse`, however, additional JDBC drivers have to be downloaded and put in the `plugins` folders, which is exactly what the `metabase-init` container is for.


**3.** After the `metabase-app` container is in a healthy state, you can acccess Metabase at:
```shell
open http://localhost:3000/
```


## TODO:
- [x] Bootstrap Apache Superset infrastructure in Docker
- [x] Bootstrap Metabase infrastructure in Docker
- [ ] Build data viz for NYC Taxi Dataset on Superset
- [ ] Build data viz for NYC Taxi Dataset on Metabase