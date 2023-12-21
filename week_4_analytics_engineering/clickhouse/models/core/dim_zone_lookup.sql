{{ config(schema='nyc_trip_record_data') }}

SELECT
    LocationID      as location_id,
    Borough         as borough,
    Zone            as zone,
    service_zone    as service_zone
FROM
    {{ ref('taxi_zone_lookup') }}