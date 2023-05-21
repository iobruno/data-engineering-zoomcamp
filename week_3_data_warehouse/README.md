# BigQuery Data Warehouse

This subproject is meant to create Native, and External tables from the GCS files on BigQuery.
And to explore partitioning and clustering data on native tables for optimum performance.

## Up and Running

### Developer Setup

**1.** Make sure to push the files/blobs to Google Cloud Storage, first.

You can use the [`web_csv_to_gcs.py`](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_2_workflow_orchestration/prefect/flows) from week 2 to achieve so.

**2.** Next, use the scripts on [`sql/`](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_3_data_warehouse/sql) folder to create the internal and external tables:

## TODO:
- [x] Create External tables for Federated Queries on BQ
- [x] Create Native tables based on the External tables
- [x] Implement Partitioning and Clustering on Internal Tables
