{{ config(
    schema=resolve_schema_for('staging')
) }}

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'dispatching_base_num',
        'pickup_datetime'
    ]) }}                        as trip_id,
    dispatching_base_num         as dispatching_base_num,
    affiliated_base_number       as affiliated_base_num,
    -- pickup and dropoff timestamps
    toDateTime(pickup_datetime)  as pickup_datetime,
    toDateTime(dropoff_datetime) as dropoff_datetime,
    -- trip info
    toInt16(pulocationid)        as pickup_location_id,
    toInt16(dolocationid)        as dropoff_location_id,
    sr_flag                      as shared_ride_flag
from 
    {{ source('clickhouse-federated-postgres-nyc-trip_record', 'ntl_fhv_taxi') }}
where
    dispatching_base_num is not null


-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
