{{ config(
    schema=resolve_schema_for('staging'),
    order_by='(vendor_id, pickup_datetime, pickup_location_id, dropoff_location_id)',
    engine='MergeTree()',
    settings={'allow_nullable_key': 1}
) }}

with green_taxi_trips as (
    select
        row_number() over(partition by vendor_id, lpep_pickup_datetime) as row_num,
        gt.*
    from
        {{ source('fqdb_nyc_taxi', 'green_taxi_trips') }} gt
    where
        vendor_id is not null        
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'vendor_id', 
        'lpep_pickup_datetime'
    ]) }}                                  as   trip_id,
    toInt8(vendor_id)                       as vendor_id,
    toInt8(ratecode_id)                     as ratecode_id,
    toInt16(pu_location_id)                 as pickup_location_id,
    toInt16(do_location_id)                 as dropoff_location_id,
    -- pickup and dropoff timestamps
    toDateTime(lpep_pickup_datetime)        as pickup_datetime,
    toDateTime(lpep_dropoff_datetime)       as dropoff_datetime,
    -- trip info
    toFixedString(store_and_fwd_flag, 1)    as store_and_fwd_flag,
    toInt8(passenger_count)                 as passenger_count,
    toDecimal32(trip_distance, 2)           as trip_distance,
    toInt8(trip_type)                       as trip_type,
    -- payment info
    toDecimal256(fare_amount, 8)            as fare_amount,
    toDecimal256(extra, 8)                  as extra,
    toDecimal256(mta_tax, 8)                as mta_tax,
    toDecimal256(tip_amount, 8)             as tip_amount,
    toDecimal256(tolls_amount, 8)           as tolls_amount,
    toDecimal256(ehail_fee, 8)              as ehail_fee,
    toDecimal256(improvement_surcharge, 8)  as improvement_surcharge,
    toDecimal256(congestion_surcharge, 8)   as congestion_surcharge,
    toDecimal256(total_amount, 8)           as total_amount,
    payment_type                            as payment_type,
    {{ payment_desc_of('payment_type')}}    as payment_type_desc
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
