{{ config(materialize='table') }}


WITH fhv_tripdata AS (
    SELECT
        dispatching_base_num,
        affiliated_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        shared_ride_flag,
        ROW_NUMBER() OVER( PARTITION BY dispatching_base_num, pickup_datetime ) AS row_num
    FROM
        {{ ref('stg_fhv_tripdata') }}
),

lookup_zones AS (
    SELECT *
    FROM {{ ref('dim_zone_lookup' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.dispatching_base_num,
    t.affiliated_base_num,
    t.pickup_location_id        AS pickup_location_id,
    pickup.borough              AS pickup_borough,
    pickup.zone                 AS pickup_zone,
    pickup.service_zone         AS pickup_service_zone,
    t.dropoff_location_id       AS dropoff_location_id,
    dropoff.borough             AS dropoff_borough,
    dropoff.zone                AS dropoff_zone,
    dropoff.service_zone        AS dropoff_service_zone,
    t.shared_ride_flag,
    t.pickup_datetime,
    t.dropoff_datetime

FROM fhv_tripdata t
INNER JOIN lookup_zones pickup  ON t.pickup_location_id  = pickup.location_id
INNER JOIN lookup_zones dropoff ON t.dropoff_location_id = dropoff.location_id
WHERE t.row_num = 1
