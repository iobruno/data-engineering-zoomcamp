{{ config(materialized='view') }}


SELECT
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime', 'PUlocationID']) }} as trip_id,
    dispatching_base_num as dispatching_base_num,    
    Affiliated_base_number as affiliated_base_num,
    pickup_datetime,
    dropOff_datetime as dropoff_datetime,
    PUlocationID as pickup_location_id,
    DOlocationID as dropoff_location_id,
    SR_Flag as shared_ride_flag
FROM 
    {{ source('staging', 'fhv_tripdata') }}


-- Run as:
--  dbt build --select stg_green_tripdata --var 'is_test_run: true'
--  dbt run --select stg_green_tripdata --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

    LIMIT 100

{% endif %}