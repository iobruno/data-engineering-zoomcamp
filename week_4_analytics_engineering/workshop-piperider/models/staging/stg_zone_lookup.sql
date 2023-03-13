{{ config(materialized='view') }}

SELECT
    -- identifier
    LocationID                              AS location_id,

    -- location
    Borough                                 AS borough,
    Zone                                    AS zone,
    REPLACE(service_zone, 'Boro', 'Green')  AS service_zone

FROM {{ source('parquet', 'zone_lookup') }}
