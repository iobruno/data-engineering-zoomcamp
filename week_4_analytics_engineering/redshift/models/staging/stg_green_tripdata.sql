{{ config(
    schema='stg_' ~ env_var('DBT_REDSHIFT_SCHEMA'))
}}

SELECT
    -- identifiers
    {{ 
        dbt_utils.generate_surrogate_key([
            'VendorID',
            'lpep_pickup_datetime'
        ])
    }}                      as trip_id,
    VendorID                as vendor_id,
    RatecodeID              as ratecode_id,
    PULocationID            as pickup_location_id,
    DOLocationID            as dropoff_location_id,
    -- pickup and dropoff timestamps
    lpep_pickup_datetime    as pickup_datetime,
    lpep_dropoff_datetime   as dropoff_datetime,
    -- trip info
    store_and_fwd_flag      as store_and_fwd_flag,
    passenger_count         as passenger_count,
    trip_distance           as trip_distance,
    trip_type               as trip_type,
    -- payment info
    fare_amount             as fare_amount,
    extra                   as extra,
    mta_tax                 as mta_tax,
    tip_amount              as tip_amount,
    tolls_amount            as tolls_amount,
    ehail_fee               as ehail_fee,
    improvement_surcharge   as improvement_surcharge,
    congestion_surcharge    as congestion_surcharge,
    total_amount            as total_amount,
    payment_type            as payment_type
FROM 
    {{ source('redshift-raw-nyc-trip_record', 'green') }}


-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
    LIMIT 100
{% endif %}