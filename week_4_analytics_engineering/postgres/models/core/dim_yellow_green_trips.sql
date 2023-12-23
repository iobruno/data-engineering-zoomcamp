{{ config(
    schema=env_var('DBT_POSTGRES_SCHEMA'))
}}

WITH green_tripdata as (
    SELECT
        row_number() OVER(PARTITION BY vendor_id, pickup_datetime) as row_num,
        g.*, 
        'green' as service_type
    FROM
        {{ ref('stg_green_tripdata') }} g
    WHERE
        vendor_id IS NOT NULL
),

yellow_tripdata as (
    SELECT
        row_number() OVER ( PARTITION BY vendor_id, pickup_datetime ) as row_num,
        y.*, 
        'yellow' as service_type
    FROM
        {{ ref('stg_yellow_tripdata') }} y
    WHERE
        vendor_id IS NOT NULL
),

all_tripdata as (
    SELECT * FROM green_tripdata WHERE row_num = 1
    UNION ALL
    SELECT * FROM yellow_tripdata WHERE row_num = 1
),

lookup_zones as (
    SELECT * FROM {{ ref('dim_zone_lookup' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.trip_id                                   as trip_id,
    t.vendor_id                                 as vendor_id,
    t.service_type                              as service_type,
    t.ratecode_id                               as ratecode_id,
    t.pickup_location_id                        as pickup_location_id,
    pickup.borough                              as pickup_borough,
    pickup.zone                                 as pickup_zone,
    t.dropoff_location_id                       as dropoff_location_id,
    dropoff.borough                             as dropoff_borough,
    dropoff.zone                                as dropoff_zone,
    t.pickup_datetime                           as pickup_datetime,
    t.dropoff_datetime                          as dropoff_datetime,
    t.store_and_fwd_flag                        as store_and_fwd_flag,
    t.passenger_count                           as passenger_count,
    t.trip_distance                             as trip_distance,
    t.trip_type                                 as trip_type,
    CAST(t.fare_amount as NUMERIC)              as fare_amount,
    CAST(t.extra as NUMERIC)                    as extra,
    CAST(t.mta_tax as NUMERIC)                  as mta_tax,
    CAST(t.tip_amount as NUMERIC)               as tip_amount,
    CAST(t.tolls_amount as NUMERIC)             as tolls_amount,
    CAST(t.ehail_fee as NUMERIC)                as ehail_fee,
    CAST(t.improvement_surcharge as NUMERIC)    as improvement_surcharge,
    CAST(t.congestion_surcharge as NUMERIC)     as congestion_surcharge,
    CAST(t.total_amount as NUMERIC)             as total_amount,
    t.payment_type                              as payment_type
FROM 
    all_tripdata t
INNER JOIN lookup_zones pickup  
    ON t.pickup_location_id  = pickup.location_id
INNER JOIN lookup_zones dropoff 
    ON t.dropoff_location_id = dropoff.location_id