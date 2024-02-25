{{ config(
    schema=resolve_schema_for('core'),
    order_by='(location_id, borough)',
    engine='MergeTree()',
    settings={'allow_nullable_key': 1}
) }}

select
    LocationID      as location_id,
    Borough         as borough,
    Zone            as zone,
    service_zone    as service_zone
from 
    {{ ref('taxi_zone_lookup') }}
