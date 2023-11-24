{{ config(materialized='view') }}

SELECT
    -- identifiers
    {{
        dbt_utils.generate_surrogate_key([
            'dispatching_base_num',
            'pickup_datetime'
        ])
    }}                      AS trip_id,
    dispatching_base_num    AS dispatching_base_num,
    Affiliated_base_number  AS affiliated_base_num,

    -- pickup and dropoff timestamps
    pickup_datetime,
    dropOff_datetime        AS dropoff_datetime,

    -- trip info
    PUlocationID            AS pickup_location_id,
    DOlocationID            AS dropoff_location_id,
    SR_Flag                 AS shared_ride_flag

FROM {{ source('parquet', 'fhv') }}
