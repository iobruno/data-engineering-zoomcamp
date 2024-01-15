# Data Visualzation with Superset

![Superset](https://img.shields.io/badge/Superset-0A2933?style=flat&logo=apache&logoColor=F8FDFF&labelColor=0A2933)
![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)
![Redshift](https://img.shields.io/badge/AWS_Redshift-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)
![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Tech Stack
- [Apache Superset](https://superset.apache.org/)
- [Docker](https://docs.docker.com/get-docker/)


## Up & Running

### Superset

**0.** (Optional) Pre-loaded examples (demo charts/dashboards):

Superset can be bootstrapped with pre-loaded example charts and dashboards. In order to enable that:
```shell
export SUPERSET_LOAD_EXAMPLES=yes
```

Database Migrations and `load_examples` processes are run everytime by the initContainer `superset-init` in [docker-compose.yml file](./docker-compose.yml), which all other superset-services depend on. 

Be make sure to `unset SUPERSET_LOAD_EXAMPLES` or `export SUPERSET_LOAD_EXAMPLES=no` after the first run of `superset-init` is completed successfully, as the `load_examples` alone might take a few minutes.

**1.** Spin up Apache Superset infrastructure with:
```shell
docker compose up -d
```


**2.** Additional database drivers:

Superset supports PostgreSQL, MySQL and out-of-the-box. To enable additional data sources, include the respective SQLAlchemy driver as a dependency on [requirements-local.txt](./superset/requirements-local.txt). 

The complete list of supported data sources can be found [here](https://superset.apache.org/docs/databases/installing-database-drivers/).

```python
sqlalchemy-bigquery==1.9.0
sqlalchemy-redshift==0.8.14
clickhouse-connect==0.6.23
```


## TODO:
- [x] Bootstrap Apache Superset infrastructure in Docker
- [ ] Build data viz for NYC Taxi Dataset on Superset