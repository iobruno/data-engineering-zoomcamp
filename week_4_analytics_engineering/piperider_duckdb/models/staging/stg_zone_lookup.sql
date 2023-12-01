SELECT
    LocationID          as location_id,
    Borough             as borough,
    Zone                as zone,
    REPLACE(
        service_zone,
        'Boro',
        'Green'
    )                   as service_zone
FROM
    {{ source('nyc_trip_record_data_csv', 'zone_lookup') }}