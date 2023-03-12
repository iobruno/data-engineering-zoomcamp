{{ config(materialize='table') }}


WITH fhv_tripdata AS (
    SELECT
        trip_id,
        dispatching_base_num,
        affiliated_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        shared_ride_flag
    FROM
        {{ ref('stg_fhv_tripdata') }}
),

lookup_zones AS (
    SELECT *
    FROM {{ ref('dim_zones' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.trip_id,
    t.dispatching_base_num,
    t.affiliated_base_num,
    t.pickup_location_id AS pickup_location_id,
    pu.borough AS pickup_borough,
    pu.zone AS pickup_zone,
    pu.service_zone AS pickup_service_zone,
    t.dropoff_location_id AS dropoff_location_id,
    do.borough AS dropoff_borough,
    do.zone AS dropoff_zone,
    do.service_zone AS dropoff_service_zone,
    t.shared_ride_flag,
    t.pickup_datetime,
    t.dropoff_datetime
FROM fhv_tripdata t
INNER JOIN lookup_zones pu ON t.pickup_location_id = pu.location_id
INNER JOIN lookup_zones do ON t.dropoff_location_id = do.location_id
