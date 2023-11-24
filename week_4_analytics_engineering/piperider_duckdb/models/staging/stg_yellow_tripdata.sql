{{ config(materialized='view') }}

SELECT
    -- identifiers
    {{
        dbt_utils.generate_surrogate_key([
            'VendorID',
            'tpep_pickup_datetime'
        ])
    }}                                          AS trip_id,
    VendorID                                    AS vendor_id,
    RatecodeID                                  AS ratecode_id,
    PULocationID                                AS pickup_location_id,
    DOLocationID                                AS dropoff_location_id,

    -- pickup and dropoff timestamps
    tpep_pickup_datetime                        AS pickup_datetime,
    tpep_dropoff_datetime                       AS dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    1                                           AS trip_type, -- yellow cabs are always street-hail

    -- payment info
    fare_amount                                 AS fare_amount,
    extra                                       AS extra,
    mta_tax                                     AS mta_tax,
    tip_amount                                  AS tip_amount,
    tolls_amount                                AS tolls_amount,
    0                                           AS ehail_fee, -- it does not apply for yellow cabs
    improvement_surcharge                       AS improvement_surcharge,
    congestion_surcharge                        AS congestion_surcharge,
    total_amount                                AS total_amount,
    payment_type                                AS payment_type,
    {{ payment_type_desc_for('payment_type') }} AS payment_type_desc

FROM {{ source('parquet', 'yellow') }}
