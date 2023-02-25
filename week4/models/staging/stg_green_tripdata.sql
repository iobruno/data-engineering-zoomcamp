{{ config(materialized='view') }}


WITH green_trip_data AS (
    SELECT
        *, 
        ROW_NUMBER() OVER(PARTITION BY VendorID, lpep_pickup_datetime) as row_num
    FROM
        {{ source('staging', 'green_tripdata') }}
)

SELECT 
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['VendorID', 'lpep_pickup_datetime']) }} as trip_id,
    VendorID as vendor_id,
    RatecodeID as ratecode_id,
    PULocationID as pickup_location_id,
    DOLocationID as dropoff_location_id,

    -- pickup and dropoff timestamps
    lpep_pickup_datetime as pickup_datetime,
    lpep_dropoff_datetime as dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    trip_type,

    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(ehail_fee as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(congestion_surcharge as numeric) as congestion_surcharge,
    cast(total_amount as numeric) as total_amount,
    cast(payment_type as integer) as payment_type,
    {{ resolve_payment_type_desc_for('payment_type') }} as payment_type_desc, 

FROM 
    green_trip_data

WHERE 
    VendorID IS NOT NULL
    AND row_num = 1

-- Run as:
--  dbt build --select stg_green_tripdata --var 'is_test_run: true'
--  dbt run --select stg_green_tripdata --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}