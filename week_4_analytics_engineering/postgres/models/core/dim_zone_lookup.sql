{{ config(
    schema=env_var('DBT_POSTGRES_SCHEMA'))
}}

SELECT
    locationid      as location_id,
    borough         as borough,
    zone            as zone,
    service_zone    as service_zone
FROM
    {{ ref('taxi_zone_lookup') }}