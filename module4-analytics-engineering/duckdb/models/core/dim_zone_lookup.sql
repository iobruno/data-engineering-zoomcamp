SELECT
    location_id,
    borough,
    zone,
    service_zone
FROM
    {{ ref('stg_zone_lookup') }}