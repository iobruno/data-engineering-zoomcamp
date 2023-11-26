-- PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.green`
PARTITION BY DATE(lpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_green`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.yellow`
PARTITION BY DATE(tpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_yellow`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.fhv`
PARTITION BY DATE(pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_fhv`
);


-- NON-PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.fhvhv`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_fhvhv`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.stg_nyc_trip_record_data.zone_lookup`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.stg_nyc_trip_record_data.ext_zone_lookup`
);
