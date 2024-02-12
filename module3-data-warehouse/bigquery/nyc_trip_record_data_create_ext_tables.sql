-- EXTERNAL TABLES FROM PARQUET
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc.ext_green`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/green_taxi_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc.ext_yellow`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/yellow_taxi_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc.ext_fhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/fhv_taxi_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc.ext_fhvhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/fhvhv_taxi_data/*.parquet"]
);

-- EXTERNAL TABLES FROM CSV
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc.ext_zone_lookup`
OPTIONS (
    format = "CSV",
    uris = ["gs://iobruno-lakehouse-raw/nyc_trip_record_data/zone_lookup/*.csv.gz"]
);
