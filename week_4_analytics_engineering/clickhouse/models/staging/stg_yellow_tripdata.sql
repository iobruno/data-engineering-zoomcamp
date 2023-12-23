{{ config(
    schema='stg_' ~ env_var('DBT_CLICKHOUSE_SCHEMA'),
    materialized='table')
}}

SELECT
    -- identifiers
    toInt8(vendorid)                        as vendor_id,
    toInt8(ratecodeid)                      as ratecode_id,
    toInt16(pulocationid)                   as pickup_location_id,
    toInt16(dolocationid)                   as dropoff_location_id,
    -- pickup and dropoff timestamps
    toDateTime(tpep_pickup_datetime)        as pickup_datetime,
    toDateTime(tpep_dropoff_datetime)       as dropoff_datetime,
    -- trip info
    toFixedString(store_and_fwd_flag, 1)    as store_and_fwd_flag,
    toInt8(passenger_count)                 as passenger_count,
    toDecimal32(trip_distance, 2)           as trip_distance,
    toInt8(1)                               as trip_type, -- yellow cabs are always street-hail
    -- payment info
    toDecimal256(fare_amount, 8)            as fare_amount,
    toDecimal256(extra, 8)                  as extra,
    toDecimal256(mta_tax, 8)                as mta_tax,
    toDecimal256(tip_amount, 8)             as tip_amount,
    toDecimal256(tolls_amount, 8)           as tolls_amount,
    toDecimal256(0, 8)                      as ehail_fee, -- it does not apply for yellow cabs
    toDecimal256(improvement_surcharge, 8)  as improvement_surcharge,
    toDecimal256(congestion_surcharge, 8)   as congestion_surcharge,
    toDecimal256(total_amount, 8)           as total_amount,
    toDecimal256(payment_type, 8)           as payment_type,
    {{ 
        payment_type_desc_for('payment_type')
    }}                                      as payment_type_desc
FROM 
    {{ source('postgres-raw-nyc-trip_record', 'ntl_yellow_taxi') }}


-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
    LIMIT 1000
{% endif %}