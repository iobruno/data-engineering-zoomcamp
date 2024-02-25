{{ config(
    schema=resolve_schema_for('staging')
) }}

with yellow_taxi_trips as (
    select
        row_number() over(partition by vendor_id, tpep_pickup_datetime) as row_num,
        yt.*
    from
        {{ source('raw_nyc_tlc_record_data', 'yellow_taxi_trips') }} yt
    where
        vendor_id is not null        
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'vendor_id', 
        'tpep_pickup_datetime'
    ]) }}                                   as trip_id,
    vendor_id                               as vendor_id,
    ratecode_id                             as ratecode_id,
    pu_location_id                          as pickup_location_id,
    do_location_id                          as dropoff_location_id,
    -- pickup and dropoff timestamps
    tpep_pickup_datetime                    as pickup_datetime,
    tpep_dropoff_datetime                   as dropoff_datetime,
    -- trip info
    store_and_fwd_flag                      as store_and_fwd_flag,
    passenger_count                         as passenger_count,
    trip_distance                           as trip_distance,
    1                                       as trip_type, -- yellow cabs are always street-hail
    -- payment info
    cast(fare_amount as numeric)            as fare_amount,
    cast(extra as numeric)                  as extra,
    cast(mta_tax as numeric)                as mta_tax,
    cast(tip_amount as numeric)             as tip_amount,
    cast(tolls_amount as numeric)           as tolls_amount,
    cast(0 as numeric)                      as ehail_fee, -- it does not apply for yellow cabs
    cast(improvement_surcharge as numeric)  as improvement_surcharge,
    cast(congestion_surcharge as numeric)   as congestion_surcharge,
    cast(total_amount as numeric)           as total_amount,
    payment_type                            as payment_type,
    {{ payment_desc_of('payment_type') }}   as payment_type_desc
from 
    yellow_taxi_trips
where
    row_num = 1

-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
