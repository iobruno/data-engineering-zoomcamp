-- EXTERNAL TABLES FROM PARQUET
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_record_data.ext_green_taxi`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_trip_record_data/green_taxi/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_record_data.ext_yellow_taxi`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_trip_record_data/yellow_taxi/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_record_data.ext_fhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_trip_record_data/fhv/*.parquet"]
);

CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_record_data.ext_hvfhv`
OPTIONS (
    format = "PARQUET",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_trip_record_data/hvfhv/*.parquet"]
);

-- EXTERNAL TABLES FROM CSV
CREATE OR REPLACE EXTERNAL TABLE `iobruno-gcp-labs.raw_nyc_tlc_record_data.ext_zone_lookup`
OPTIONS (
    format = "CSV",
    uris = ["gs://iobruno-lakehouse-raw/nyc_tlc_trip_record_data/zone_lookup/*.csv.gz"]
);
