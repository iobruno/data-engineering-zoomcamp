{{ config(
    schema=resolve_schema_for('core')
) }}

with green_taxi_trips as (
    select
        gt.*,
        'green' as service_type
    from 
        {{ ref('stg_green_tripdata') }} gt
),

yellow_taxi_trips as (
    select
        yt.*,
        'yellow' as service_type
    from 
        {{ ref('stg_yellow_tripdata') }} yt
),

taxi_trips as (
    select * from green_taxi_trips
    union all 
    select * from yellow_taxi_trips
),

lookup_zones as (
    select * 
    from {{ ref('dim_zone_lookup' )}} 
    where borough != 'Unknown'
)

select
    tt.trip_id                                  as trip_id,
    tt.vendor_id                                as vendor_id,
    tt.service_type                             as service_type,
    tt.ratecode_id                              as ratecode_id,
    tt.pickup_location_id                       as pickup_location_id,
    pickup.borough                              as pickup_borough,
    pickup.zone                                 as pickup_zone,
    tt.dropoff_location_id                      as dropoff_location_id,
    dropoff.borough                             as dropoff_borough,
    dropoff.zone                                as dropoff_zone,
    tt.pickup_datetime                          as pickup_datetime,
    tt.dropoff_datetime                         as dropoff_datetime,
    tt.store_and_fwd_flag                       as store_and_fwd_flag,
    tt.passenger_count                          as passenger_count,
    tt.trip_distance                            as trip_distance,
    tt.trip_type                                as trip_type,
    cast(tt.fare_amount as numeric)             as fare_amount,
    cast(tt.extra as numeric)                   as extra,
    cast(tt.mta_tax as numeric)                 as mta_tax,
    cast(tt.tip_amount as numeric)              as tip_amount,
    cast(tt.tolls_amount as numeric)            as tolls_amount,
    cast(tt.ehail_fee as numeric)               as ehail_fee,
    cast(tt.improvement_surcharge as numeric)   as improvement_surcharge,
    cast(tt.congestion_surcharge as numeric)    as congestion_surcharge,
    cast(tt.total_amount as numeric)            as total_amount,
    t.payment_type                              as payment_type,
    t.payment_type_desc                         as payment_type_description
from 
    taxi_trips tt
inner join 
    lookup_zones pickup on tt.pickup_location_id  = pickup.location_id
inner join 
    lookup_zones dropoff on tt.dropoff_location_id = dropoff.location_id
