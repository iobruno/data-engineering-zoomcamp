# BigQuery Data Warehouse

![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)
![GCP](https://img.shields.io/badge/Google_Cloud-3772FF?style=flat&logo=googlecloud&logoColor=white&labelColor=3772FF)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project creates Native and External tables from GCS files on BigQuery, emphasizing optimal performance through the exploration of partitioning and clustering techniques on native tables


## Up and Running

### Developer Setup

**1.** Make sure to push the files/blobs to Google Cloud Storage, first.

You can use the [`prefect/flows/web_csv_to_gcs.py`](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week_2_workflow_orchestration/prefect/flows/) to achieve so.

**2.** Next, use the scripts on [`sql/`](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_3_data_warehouse/sql) folder to create the internal and external tables:


## TODO:
- [x] Create External tables for Federated Queries on BQ
- [x] Create Native tables based on the External tables
- [x] Implement Partitioning and Clustering on Internal Tables
