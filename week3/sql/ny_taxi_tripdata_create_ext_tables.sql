CREATE OR REPLACE EXTERNAL TABLE `iobruno-training-gcp.dtc_ny_taxi_tripdata_staging.ext_green_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_datalake_raw/dtc_ny_taxi_tripdata/green/*.parquet.snappy"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-training-gcp.dtc_ny_taxi_tripdata_staging.ext_yellow_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_datalake_raw/dtc_ny_taxi_tripdata/yellow/*.parquet.snappy"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-training-gcp.dtc_ny_taxi_tripdata_staging.ext_fhv_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno_datalake_raw/dtc_ny_taxi_tripdata/fhv/*.parquet.snappy"]
);
