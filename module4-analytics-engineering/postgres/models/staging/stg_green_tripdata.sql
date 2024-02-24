{{ config(
    schema=resolve_schema_for('staging')
) }}

with green_taxi_trips as (
    select
        row_number() over(partition by vendor_id, lpep_pickup_datetime) as row_num,
        gt.*
    from
        {{ source('raw_nyc_tlc_record_data', 'green_taxi_trips') }} gt
    where
        vendor_id is not null        
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'vendor_id',
        'lpep_pickup_datetime'
    ]) }}                                   as trip_id,
    vendor_id                               as vendor_id,
    ratecode_id                             as ratecode_id,
    pu_location_id                          as pickup_location_id,
    do_location_id                          as dropoff_location_id,
    -- pickup and dropoff timestamps
    lpep_pickup_datetime                    as pickup_datetime,
    lpep_dropoff_datetime                   as dropoff_datetime,
    -- trip info
    store_and_fwd_flag                      as store_and_fwd_flag,
    passenger_count                         as passenger_count,
    trip_distance                           as trip_distance,
    trip_type                               as trip_type,
    -- payment info
    fare_amount                             as fare_amount,
    extra                                   as extra,
    mta_tax                                 as mta_tax,
    tip_amount                              as tip_amount,
    tolls_amount                            as tolls_amount,
    ehail_fee                               as ehail_fee,
    improvement_surcharge                   as improvement_surcharge,
    congestion_surcharge                    as congestion_surcharge,
    total_amount                            as total_amount,
    payment_type                            as payment_type,
    {{ payment_desc_of('payment_type') }}   as payment_type_desc
from 
    green_taxi_trips
where
    row_num = 1

-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
