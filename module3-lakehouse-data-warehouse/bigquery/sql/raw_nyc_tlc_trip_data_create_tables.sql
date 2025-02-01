-- PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.green_taxi`
PARTITION BY DATE(lpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_green_taxi`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.yellow_taxi`
PARTITION BY DATE(tpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_yellow_taxi`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.fhv`
PARTITION BY DATE(pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_fhv`
);


-- NON-PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.hvfhv`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_hvfhv`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc_trip_data.zone_lookup`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc_trip_data.ext_zone_lookup`
);
