{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_trips as (
    select
        dispatching_base_num,
        affiliated_base_num,
        pickup_datetime,
        dropoff_datetime,
        pickup_location_id,
        dropoff_location_id,
        shared_ride_flag
    from 
        {{ ref('stg_fhv_tripdata') }}
),

lookup_zones as (
    select * 
    from {{ ref('dim_zone_lookup' )}} 
    where borough != 'Unknown'
)

select
    ft.dispatching_base_num as dispatching_base_num,
    ft.affiliated_base_num  as affiliated_base_num,
    ft.pickup_location_id   as pickup_location_id,
    pickup.borough          as pickup_borough,
    pickup.zone             as pickup_zone,
    pickup.service_zone     as pickup_service_zone,
    ft.dropoff_location_id  as dropoff_location_id,
    dropoff.borough         as dropoff_borough,
    dropoff.zone            as dropoff_zone,
    dropoff.service_zone    as dropoff_service_zone,
    ft.shared_ride_flag     as shared_ride_flag,
    ft.pickup_datetime      as pickup_datetime,
    ft.dropoff_datetime     as dropoff_datetime
from  
    fhv_trips ft
inner join 
    lookup_zones pickup  on ft.pickup_location_id  = pickup.location_id
inner join 
    lookup_zones dropoff on ft.dropoff_location_id = dropoff.location_id
