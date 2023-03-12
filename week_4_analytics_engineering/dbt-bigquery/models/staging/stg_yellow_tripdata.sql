{{ config(materialized='view') }}


WITH yellow_trip_data AS (
    SELECT
        -- identifiers
        VendorID AS vendor_id,
        RatecodeID AS ratecode_id,
        PULocationID AS pickup_location_id,
        DOLocationID AS dropoff_location_id,

        -- pickup and dropoff timestamps
        tpep_pickup_datetime AS pickup_datetime,
        tpep_dropoff_datetime AS dropoff_datetime,

        -- trip info
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        1 AS trip_type, -- yellow cabs are always street-hail

        -- payment info
        CAST(fare_amount as numeric) AS fare_amount,
        CAST(extra as numeric) AS extra,
        CAST(mta_tax as numeric) AS mta_tax,
        CAST(tip_amount as numeric) AS tip_amount,
        CAST(tolls_amount as numeric) AS tolls_amount,
        CAST(0 as numeric) AS ehail_fee, -- it does not apply for yellow cabs
        CAST(improvement_surcharge as numeric) AS improvement_surcharge,
        CAST(congestion_surcharge as numeric) AS congestion_surcharge,
        CAST(total_amount as numeric) AS total_amount,
        CAST(payment_type as integer) AS payment_type,
        {{ resolve_payment_type_desc_for('payment_type') }} AS payment_type_desc,

        -- window function to help with deduplication
        ROW_NUMBER() OVER( PARTITION BY VendorID, tpep_pickup_datetime ) as row_num

    FROM
        {{ source('staging', 'yellow_tripdata') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['vendor_id', 'pickup_datetime']) }} AS trip_id,
    y.vendor_id,
    y.ratecode_id,
    y.pickup_location_id,
    y.dropoff_location_id,
    y.pickup_datetime,
    y.dropoff_datetime,
    y.store_and_fwd_flag,
    y.passenger_count,
    y.trip_distance,
    y.trip_type,
    y.fare_amount,
    y.extra,
    y.mta_tax,
    y.tip_amount,
    y.tolls_amount,
    y.ehail_fee,
    y.improvement_surcharge,
    y.congestion_surcharge,
    y.total_amount,
    y.payment_type,
    y.payment_type_desc
FROM
    yellow_trip_data y
WHERE
     row_num = 1 AND
     vendor_id IS NOT NULL

-- Run as:
--  dbt build --select stg_green_tripdata --var 'is_test_run: true'
--  dbt run --select stg_green_tripdata --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}
