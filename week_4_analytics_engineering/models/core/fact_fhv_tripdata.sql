{{ config(materialize='table') }}

WITH fhv_tripdata as (
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

lookup_zones as (
    SELECT * FROM {{ ref('dim_zones' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.trip_id,
    t.dispatching_base_num,
    t.affiliated_base_num,
    t.pickup_location_id as pickup_location_id,
    pu.borough as pickup_borough,
    pu.zone as pickup_zone,
    pu.service_zone as pickup_service_zone,
    t.dropoff_location_id as dropoff_location_id,    
    do.borough as dropoff_borough,
    do.zone as dropoff_zone,
    do.service_zone as dropoff_service_zone,
    t.shared_ride_flag,        	
    t.pickup_datetime,
    t.dropoff_datetime
FROM fhv_tripdata t
INNER JOIN lookup_zones pu ON t.pickup_location_id = pu.location_id
INNER JOIN lookup_zones do ON t.dropoff_location_id = do.location_id
