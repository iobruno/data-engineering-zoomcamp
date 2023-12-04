{{ config(schema='nyc_trip_record_data') }}

WITH fhv_tripdata as (
    SELECT
        dispatching_base_num,
        affiliated_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        shared_ride_flag,
        row_number() OVER (PARTITION BY dispatching_base_num, pickup_datetime) AS row_num
    FROM
        {{ ref('stg_fhv_tripdata') }}
),

lookup_zones AS (
    SELECT * FROM {{ ref('dim_zone_lookup' )}} 
    WHERE borough != 'Unknown'
)

SELECT
    t.dispatching_base_num  as dispatching_base_num,
    t.affiliated_base_num   as affiliated_base_num,
    t.pickup_location_id    as pickup_location_id,
    pickup.borough          as pickup_borough,
    pickup.zone             as pickup_zone,
    pickup.service_zone     as pickup_service_zone,
    t.dropoff_location_id   as dropoff_location_id,
    dropoff.borough         as dropoff_borough,
    dropoff.zone            as dropoff_zone,
    dropoff.service_zone    as dropoff_service_zone,
    t.shared_ride_flag      as shared_ride_flag,
    t.pickup_datetime       as pickup_datetime,
    t.dropoff_datetime      as dropoff_datetime
FROM 
    fhv_tripdata t
INNER JOIN lookup_zones pickup  
    ON t.pickup_location_id  = pickup.location_id
INNER JOIN lookup_zones dropoff 
    ON t.dropoff_location_id = dropoff.location_id
WHERE 
    t.row_num = 1
