{{ config(materialize='table') }}

WITH green_tripdata as (
    SELECT
        *,
        'green' as service_type
    FROM
        {{ ref('stg_green_tripdata') }}
),

yellow_tripdata as (
    SELECT
        *,
        'yellow' as service_type
    FROM
        {{ ref('stg_yellow_tripdata') }}
),

all_tripdata as (
    SELECT * from green_tripdata
    UNION ALL
    SELECT * FROM yellow_tripdata
),

lookup_zones as (
    SELECT * FROM {{ ref('dim_zones' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.trip_id,
    t.vendor_id,
    t.service_type,
    t.ratecode_id,
    t.pickup_location_id,
    pu.borough as pickup_borough,
    pu.zone as pickup_zone,
    t.dropoff_location_id,
    do.borough as dropoff_borough,
    do.zone as dropoff_zone,
    t.pickup_datetime,
    t.dropoff_datetime,
    t.store_and_fwd_flag,
    t.passenger_count,
    t.trip_distance,
    t.trip_type,
    t.fare_amount,
    t.extra,
    t.mta_tax,
    t.tip_amount,
    t.tolls_amount,
    t.ehail_fee,
    t.improvement_surcharge,
    t.total_amount,
    t.payment_type,
    t.payment_type_desc,
    t.congestion_surcharge
FROM all_tripdata t
INNER JOIN lookup_zones pu ON t.pickup_location_id  = pu.location_id
INNER JOIN lookup_zones do ON t.dropoff_location_id = do.location_id
