CREATE OR REPLACE TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.green_tripdata`
PARTITION BY DATE(lpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_green_tripdata`
);


CREATE OR REPLACE TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.yellow_tripdata`
PARTITION BY DATE(tpep_pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_yellow_tripdata`
);

CREATE OR REPLACE TABLE `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.fhv_tripdata`
PARTITION BY DATE(pickup_datetime)
AS (
    SELECT *
    FROM `iobruno-data-eng-zoomcamp.dtc_ny_taxi_tripdata_staging.ext_fhv_tripdata`
);
