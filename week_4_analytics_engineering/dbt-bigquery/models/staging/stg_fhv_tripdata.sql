{{ config(materialized='view') }}


SELECT
    -- surrogate_key
    {{
        dbt_utils.generate_surrogate_key([
            'dispatching_base_num',
            'pickup_datetime',
            'PUlocationID'
        ])
    }} AS trip_id,

    dispatching_base_num AS dispatching_base_num,
    Affiliated_base_number AS affiliated_base_num,
    pickup_datetime,
    dropOff_datetime AS dropoff_datetime,
    PUlocationID AS pickup_location_id,
    DOlocationID AS dropoff_location_id,
    SR_Flag AS shared_ride_flag

FROM
    {{ source('staging', 'fhv_tripdata') }}


-- Run as:
--  dbt build --select stg_green_tripdata --var 'is_test_run: true'
--  dbt run --select stg_green_tripdata --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}
