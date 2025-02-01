-- EXTERNAL TABLES FROM PARQUET
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_green_taxi`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/green_trip_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_yellow_taxi`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/yellow_trip_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_fhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/fhv_trip_data/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_hvfhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/hvfhv_trip_data/*.parquet"]
);

-- EXTERNAL TABLES FROM CSV
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_zone_lookup`
OPTIONS (
    format = "CSV",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_dataset/zone_lookup/*.csv.gz"]
);
