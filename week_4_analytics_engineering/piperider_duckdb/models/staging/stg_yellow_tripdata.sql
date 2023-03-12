{{ config(materialized='table') }}

SELECT *
FROM {{ source('parquet', 'yellow') }}
