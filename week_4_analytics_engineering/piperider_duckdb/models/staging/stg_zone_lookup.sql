{{ config(materialized='table') }}

SELECT *
FROM {{ source('parquet', 'zone_lookup') }}
