{{ config(
    schema=resolve_schema_for('staging'),
    order_by='(pickup_location_id, dropoff_location_id)',
    engine='MergeTree()',
    settings={'allow_nullable_key': 1}
) }}

with fhv_trips as (
    select
        fhv.*
    from
        {{ source('fqdb_nyc_taxi', 'fhv_trips') }} fhv
    where
        dispatching_base_num is not null        
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'dispatching_base_num',
        'pickup_datetime'
    ]) }}                           as trip_id,
    dispatching_base_num            as dispatching_base_num,
    affiliated_base_number          as affiliated_base_num,
    -- pickup and dropoff timestamps
    toDateTime(pickup_datetime)     as pickup_datetime,
    toDateTime(dropoff_datetime)    as dropoff_datetime,
    -- trip info
    toInt16(pu_location_id)         as pickup_location_id,
    toInt16(do_location_id)         as dropoff_location_id,
    sr_flag                         as shared_ride_flag
from 
    fhv_trips

-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
