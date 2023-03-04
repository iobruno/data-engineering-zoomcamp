# Data Engineering Zoomcamp - Cohort 2023

- [Course Playlist on Youtube](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

**Week 1: Introduction & Prerequisites**:

- [Homework Part A - Docker & SQL](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_1a.md)
- [Homework Part B - Terraform](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_1b.md)
- [Project: Postgres Ingestion from CSV](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_1_basics_n_setup/postgres_ingest)
- [Project: Terraform for Google Cloud Storage and BigQuery](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_1_basics_n_setup/terraform)

**Week 2: Workflow Orchestration**:
- [Homework - Prefect Orchestration](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_2.md)
- [Project: Prefect Flows](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_2_workflow_orchestration/prefect)
  - [Flow: CSV Dataset to Postgres](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_2_workflow_orchestration/prefect/flows/pg_ingest.py)
  - [Flow: CSV Dataset to GCS .parquet](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_2_workflow_orchestration/prefect/flows/web_csv_to_gcs.py)
  - [Flow: GCS Bucket to BigQuery](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_2_workflow_orchestration/prefect/flows/gcs_to_bigquery.py)

**Week 3: Data Warehouse**:
- [Homework - Data Warehouse with BigQuery](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_3.md)
- [Project: Prefect Flow: upload_from_dataframe](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_3_data_warehouse/prefect/flows/web_csv_to_gcs.py)

**Week 4: Analytics Engineering**:
- [Homework - Analytics Engineering](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_4.md)
- [Project: dbt Modeling](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_4_analytics_engineering)

**Week 5: Batch processing**:
- [Homework Answers - Batch Processing](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/homework/week_5.md)
- [Homework Project - PySpark Jupyter](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_5_batch_processing/pyspark/notebooks/pyspark_homework.ipynb)
- [PySpark Project: FHV with Zone Lookup](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_5_batch_processing/pyspark)
- Jupyter Playgrounds:
  - [PySpark + SparkSQL](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_5_batch_processing/pyspark/notebooks/pyspark_playground.ipynb)
  - [PyFlink + FlinkSQL](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_5_batch_processing/pyflink/notebooks/pyflink_playground.ipynb)

Week 6: Streaming

Week 7, 8 & 9: Project
