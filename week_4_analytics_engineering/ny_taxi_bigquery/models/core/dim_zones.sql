{{ config(materialize='table') }}

SELECT
    LocationID as location_id,
    Borough as borough,
    Zone as zone,
    REPLACE(service_zone, 'Boro', 'Green') as service_zone
FROM     
    {{ ref('taxi_zone_lookup') }}
