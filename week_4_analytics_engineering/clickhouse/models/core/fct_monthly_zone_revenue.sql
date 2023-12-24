{{ config(
    schema=env_var('DBT_CLICKHOUSE_SCHEMA'),
    materialized='table')
}}

SELECT
    -- Revenue Grouping
    pickup_zone                           as revenue_zone,
    date_trunc('month', pickup_datetime)  as revenue_month,
    service_type                          as service_type,
    -- Revenue Calculations
    ROUND(SUM(fare_amount), 2)             as revenue_monthly_fare,
    ROUND(SUM(extra), 2)                   as revenue_monthly_extra,
    ROUND(SUM(mta_tax), 2)                 as revenue_monthly_mta_tax,
    ROUND(SUM(tip_amount), 2)              as revenue_monthly_tip_amount,
    ROUND(SUM(tolls_amount), 2)            as revenue_monthly_tolls_amount,
    ROUND(SUM(ehail_fee), 2)               as revenue_monthly_ehail_fee,
    ROUND(SUM(improvement_surcharge), 2)   as revenue_monthly_improvement_surcharge,
    ROUND(SUM(total_amount), 2)            as revenue_monthly_total_amount,
    ROUND(SUM(congestion_surcharge), 2)    as revenue_monthly_congestion_surcharge
FROM
    {{ ref('dim_yellow_green_trips') }}
GROUP BY
    pickup_zone,
    date_trunc('month', pickup_datetime),
    service_type