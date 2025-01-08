# BigQuery Data Warehouse

[![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![CloudStorage](https://img.shields.io/badge/Google_Cloud_Storage_-3772FF?style=flat&logo=googlecloudstorage&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/storage)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This project creates Native and External tables from GCS files on BigQuery,  
- It emphasizes optimal performance through Partitioning and Clustering on Native tables
- And serves as a Query Engine for creating External tables to query Parquet and CSV data in GCS


## Getting Started

**1.** Make sure to push the files/blobs to Google Cloud Storage, first.  
You can use the [`web_csv_to_gcs.py`](../../module2-workflow-orchestration/prefect/flows/web_csv_to_gcs.py) to achieve so.

**2.** Next, use the scripts on [`sql/`](./sql/) in this specific order:
- [Create external tables](sql/raw_nyc_tlc_trip_data_create_ext_tables.sql)
- [Create native tables](sql/raw_nyc_tlc_trip_data_create_tables.sql)


## TODO's:
- [x] Create External tables for Federated Queries
- [x] Create Native (and Partitioned tables, when appliable) from the External tables
