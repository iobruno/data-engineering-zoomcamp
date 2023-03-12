{{ config(materialized='view') }}


WITH green_trip_data AS (
    SELECT
        -- identifiers
        VendorID AS vendor_id,
        RatecodeID AS ratecode_id,
        PULocationID AS pickup_location_id,
        DOLocationID AS dropoff_location_id,

        -- pickup and dropoff timestamps
        lpep_pickup_datetime AS pickup_datetime,
        lpep_dropoff_datetime AS dropoff_datetime,

        -- trip info
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        trip_type,

        -- payment info
        CAST(fare_amount as numeric) AS fare_amount,
        CAST(extra as numeric) AS extra,
        CAST(mta_tax as numeric) AS mta_tax,
        CAST(tip_amount as numeric) AS tip_amount,
        CAST(tolls_amount as numeric) AS tolls_amount,
        CAST(ehail_fee as numeric) AS ehail_fee,
        CAST(improvement_surcharge as numeric) AS improvement_surcharge,
        CAST(congestion_surcharge as numeric) AS congestion_surcharge,
        CAST(total_amount as numeric) AS total_amount,
        CAST(payment_type as integer) AS payment_type,
        {{ resolve_payment_type_desc_for('payment_type') }} AS payment_type_desc,

        -- window function to help with deduplication
        ROW_NUMBER() OVER( PARTITION BY VendorID, lpep_pickup_datetime ) AS row_num

    FROM
        {{ source('staging', 'green_tripdata') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['vendor_id', 'pickup_datetime']) }} as trip_id,
    g.vendor_id,
    g.ratecode_id,
    g.pickup_location_id,
    g.dropoff_location_id,
    -- pickup and dropoff timestamps
    g.pickup_datetime,
    g.dropoff_datetime,
    -- trip info
    g.store_and_fwd_flag,
    g.passenger_count,
    g.trip_distance,
    g.trip_type,
    -- payment info
    g.fare_amount,
    g.extra,
    g.mta_tax,
    g.tip_amount,
    g.tolls_amount,
    g.ehail_fee,
    g.improvement_surcharge,
    g.congestion_surcharge,
    g.total_amount,
    g.payment_type,
    g.payment_type_desc
FROM
    green_trip_data g
WHERE
    row_num = 1 AND
    vendor_id IS NOT NULL

-- Run as:
--  dbt build --select stg_green_tripdata --var 'is_test_run: true'
--  dbt run --select stg_green_tripdata --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}
