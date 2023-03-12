{{ config(materialized='table') }}

SELECT *
FROM {{ source('parquet', 'fhv') }}
