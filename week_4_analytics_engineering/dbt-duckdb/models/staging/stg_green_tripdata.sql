{{ config(materialized='table') }}

SELECT *
FROM {{ source('parquet', 'green') }}
