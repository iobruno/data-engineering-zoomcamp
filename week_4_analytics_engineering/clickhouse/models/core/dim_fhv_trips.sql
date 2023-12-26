{{ config(
    schema=resolve_schema_for('core'),
    order_by='(dispatching_base_num, pickup_datetime, pickup_location_id, dropoff_location_id)',
    engine='MergeTree()',
    settings={'allow_nullable_key': 1}
) }}

with fhv_tripdata as (
    select
        dispatching_base_num,
        affiliated_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        shared_ride_flag,
        row_number() over (partition by dispatching_base_num, pickup_datetime) as row_num
    from 
        {{ ref('stg_fhv_tripdata') }}
),

lookup_zones as (
    select * from {{ ref('dim_zone_lookup' )}} where borough != 'Unknown'
)

select
    t.dispatching_base_num as dispatching_base_num,
    t.affiliated_base_num  as affiliated_base_num,
    t.pickup_location_id   as pickup_location_id,
    pickup.borough         as pickup_borough,
    pickup.zone            as pickup_zone,
    pickup.service_zone    as pickup_service_zone,
    t.dropoff_location_id  as dropoff_location_id,
    dropoff.borough        as dropoff_borough,
    dropoff.zone           as dropoff_zone,
    dropoff.service_zone   as dropoff_service_zone,
    t.shared_ride_flag     as shared_ride_flag,
    t.pickup_datetime      as pickup_datetime,
    t.dropoff_datetime     as dropoff_datetime
from  
    fhv_tripdata t
inner join 
    lookup_zones pickup  on t.pickup_location_id  = pickup.location_id
inner join 
    lookup_zones dropoff on t.dropoff_location_id = dropoff.location_id
where 
    t.row_num = 1
