# Data Engineering Zoomcamp

## Taking the course

### 2024 Cohort

* **Start**: 15 January 2024 (Monday) at 17:00 CET
* **Registration link**: https://airtable.com/shr6oVXeQvSI5HuWD
* [Cohort folder](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2024) with homeworks and deadlines

### Self-paced mode

All the materials of the course are freely available, so that you
can take the course at your own pace

* Follow the suggested syllabus (see below) week by week
* You don't need to fill in the registration form. Just start watching the videos and join Slack
* Check [FAQ](https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit?usp=sharing) if you have problems


## Syllabus 

### [Module 1: Introduction & Prerequisites](week_1_basics_n_setup):
* [pandas and SQLAlchemy](week_1_basics_n_setup/pandas_sqlalchemy)
* [Terraform for BigQuery and GCS](week_1_basics_n_setup/terraform-gcp)
* Homework

### [Module 2: Workflow Orchestration](week_2_workflow_orchestration):
* [Workflow Orchestration with Airflow](week_2_workflow_orchestration/airflow)
* [Workflow Orchestration with Mage](week_2_workflow_orchestration/mage)
* [Workflow Orchestration with Prefect](week_2_workflow_orchestration/prefect)
  * [*.csv to Postgres](week_2_workflow_orchestration/prefect/flows/sqlalchemy_ingest.py)
  * [*.csv to .parquet on GCS](week_2_workflow_orchestration/prefect/flows/web_csv_to_gcs.py)
* Homework

### [Module 3: Data Warehouse](week_3_data_warehouse)
* [BigQuery Data Warehouse](week_3_data_warehouse/bigquery)
  * [Federated Queries: External Tables](week_3_data_warehouse/bigquery/nyc_trip_record_data_create_ext_tables.sql)
  * [Partitioning Native Tables](week_3_data_warehouse/bigquery/nyc_trip_record_data_create_tables.sql)
* Lakehouse with Delta Lake/Iceberg
* Homework

### [Module 4: Analytics Engineering](week_4_analytics_engineering)
* [BigQuery and dbt](week_4_analytics_engineering/bigquery)
* [Redshift and dbt](week_4_analytics_engineering/redshift)
* Databricks and dbt
* [ClickHouse and dbt](week_4_analytics_engineering/clickhouse)
* [PostgreSQL and dbt](week_4_analytics_engineering/postgres)
* [DuckDB and dbt](week_4_analytics_engineering/duckdb)
* Data visualization with Looker Studio
* Data visualization with Superset (TBD)
* Homework

### [Module 5: Batch processing](week_5_batch_processing)
* [PySpark on Jupyter Playground](week_5_batch_processing/pyspark/notebooks/)
* PySpark (deploy-mode: 'cluster')  
* Spark + Scala
* Spark + Kotlin (TBD)
* Homework

### [Module 6: Streaming](week_6_stream_processing)
* [Kafka for Stream Processing with Kotlin](week_6_stream_processing/kotlin)
* [Kafka Streams with ksqlDB](week_6_stream_processing/ksqldb)
* Homework

### [Module 7: Capstone Project](week_7_capstone_project)
* Capstone Project
