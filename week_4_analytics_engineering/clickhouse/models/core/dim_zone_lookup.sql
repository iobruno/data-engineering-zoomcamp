{{ config(
    schema=env_var('DBT_CLICKHOUSE_SCHEMA'),
    materialized='table')
}}

SELECT
    LocationID      as location_id,
    Borough         as borough,
    Zone            as zone,
    service_zone    as service_zone
FROM
    {{ ref('taxi_zone_lookup') }}