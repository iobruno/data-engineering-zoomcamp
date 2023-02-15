CREATE OR REPLACE EXTERNAL TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_green_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_dtc_datalake_raw/green/*.parquet.snappy"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_yellow_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_dtc_datalake_raw/yellow/*.parquet.snappy"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_fhv_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_dtc_datalake_raw/fhv/*.parquet.snappy"]
);
