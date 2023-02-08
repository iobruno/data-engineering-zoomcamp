-- EXTERNAL TABLES FROM PARQUET
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.dtc_ny_taxi_tripdata_staging.ext_green_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-datalake-raw/dtc_ny_taxi_tripdata/green/*.snappy.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.dtc_ny_taxi_tripdata_staging.ext_yellow_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-datalake-raw/dtc_ny_taxi_tripdata/yellow/*.snappy.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.dtc_ny_taxi_tripdata_staging.ext_fhv_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-datalake-raw/dtc_ny_taxi_tripdata/fhv/*.snappy.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.dtc_ny_taxi_tripdata_staging.ext_fhvhv_tripdata`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-datalake-raw/dtc_ny_taxi_tripdata/fhvhv/*.snappy.parquet"]

);


-- EXTERNAL TABLES FROM CSV
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.dtc_ny_taxi_tripdata_staging.ext_zone_lookup`
OPTIONS (
    format = "CSV",
    uris = ["gs://iobruno-datalake-raw/dtc_ny_taxi_tripdata/zone_lookup/*.csv.gz"]

);
