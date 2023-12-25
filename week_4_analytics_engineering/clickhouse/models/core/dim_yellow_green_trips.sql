{{ config(
    schema=env_var('DBT_CLICKHOUSE_SCHEMA')
) }}

with green_tripdata as (
    select
        row_number() over(partition by vendor_id, pickup_datetime) as row_num,
        'green' as service_type,
        g.*
    from 
        {{ ref('stg_green_tripdata') }} g
),

yellow_tripdata as (
    select
        row_number() over (partition by vendor_id, pickup_datetime) as row_num,
        'yellow' as service_type,
        y.*
    from 
        {{ ref('stg_yellow_tripdata') }} y
),

all_tripdata as (
    select * from green_tripdata where row_num = 1    
    union all 
    select * from yellow_tripdata where row_num = 1
),

lookup_zones as (
    select * from {{ ref('dim_zone_lookup' )}} where borough != 'Unknown'
)

select
    t.trip_id               as trip_id,
    t.vendor_id             as vendor_id,
    t.service_type          as service_type,
    t.ratecode_id           as ratecode_id,
    t.pickup_location_id    as pickup_location_id,
    pickup.borough          as pickup_borough,
    pickup.zone             as pickup_zone,
    t.dropoff_location_id   as dropoff_location_id,
    dropoff.borough         as dropoff_borough,
    dropoff.zone            as dropoff_zone,
    t.pickup_datetime       as pickup_datetime,
    t.dropoff_datetime      as dropoff_datetime,
    t.store_and_fwd_flag    as store_and_fwd_flag,
    t.passenger_count       as passenger_count,
    t.trip_distance         as trip_distance,
    t.trip_type             as trip_type,
    t.fare_amount           as fare_amount,
    t.extra                 as extra,
    t.mta_tax               as mta_tax,
    t.tip_amount            as tip_amount,
    t.tolls_amount          as tolls_amount,
    t.ehail_fee             as ehail_fee,
    t.improvement_surcharge as improvement_surcharge,
    t.total_amount          as total_amount,
    t.payment_type          as payment_type,
    t.congestion_surcharge  as congestion_surcharge
from 
    all_tripdata t
inner join 
    lookup_zones pickup on t.pickup_location_id  = pickup.location_id
inner join 
    lookup_zones dropoff on t.dropoff_location_id = dropoff.location_id
