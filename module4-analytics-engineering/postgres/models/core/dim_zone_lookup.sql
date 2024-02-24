{{ config(
    schema=resolve_schema_for('core')
) }}

select
    locationid   as location_id,
    borough      as borough,
    zone         as zone,
    service_zone as service_zone
from 
    {{ ref('taxi_zone_lookup') }}
