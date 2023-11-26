-- EXTERNAL TABLES FROM PARQUET
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_green`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/green/*.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_yellow`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/yellow/*.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_fhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/fhv/*.parquet"]

);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_fhvhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/fhvhv/*.parquet"]

);


-- EXTERNAL TABLES FROM CSV
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_zone_lookup`
OPTIONS (
    format = "CSV",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/zone_lookup/*.csv.gz"]

);
