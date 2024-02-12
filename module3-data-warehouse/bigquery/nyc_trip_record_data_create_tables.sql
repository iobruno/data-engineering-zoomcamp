-- PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc.green`
PARTITION BY DATE(lpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc.ext_green`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc.yellow`
PARTITION BY DATE(tpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc.ext_yellow`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc.fhv`
PARTITION BY DATE(pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc.ext_fhv`
);


-- NON-PARTITIONED TABLES
CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc.fhvhv`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc.ext_fhvhv`
);


CREATE OR REPLACE TABLE `iobruno-gcp-labs.raw_nyc_tlc.zone_lookup`
AS (
    SELECT *
    FROM `iobruno-gcp-labs.raw_nyc_tlc.ext_zone_lookup`
);
