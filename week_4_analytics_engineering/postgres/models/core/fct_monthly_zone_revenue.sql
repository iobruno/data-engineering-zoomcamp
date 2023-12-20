{{ config(schema='nyc_trip_record_data') }}

SELECT
    -- Revenue Grouping
    pickup_zone                                             as revenue_zone,
    date_trunc('month', pickup_datetime)                    as revenue_month,
    service_type                                            as service_type,
    -- Revenue Calculations
    ROUND(CAST(SUM(fare_amount) as NUMERIC), 2)             as revenue_monthly_fare,
    ROUND(CAST(SUM(extra) as NUMERIC), 2)                   as revenue_monthly_extra,
    ROUND(CAST(SUM(mta_tax) as NUMERIC), 2)                 as revenue_monthly_mta_tax,
    ROUND(CAST(SUM(tip_amount) as NUMERIC), 2)              as revenue_monthly_tip_amount,
    ROUND(CAST(SUM(tolls_amount) as NUMERIC), 2)            as revenue_monthly_tolls_amount,
    ROUND(CAST(SUM(ehail_fee) as NUMERIC), 2)               as revenue_monthly_ehail_fee,
    ROUND(CAST(SUM(improvement_surcharge) as NUMERIC), 2)   as revenue_monthly_improvement_surcharge,
    ROUND(CAST(SUM(total_amount) as NUMERIC), 2)            as revenue_monthly_total_amount,
    ROUND(CAST(SUM(congestion_surcharge) as NUMERIC), 2)    as revenue_monthly_congestion_surcharge
FROM
    "nyc_taxi"."staging_nyc_trip_record_data"."dim_yellow_green_trips"
GROUP BY
    pickup_zone,
    date_trunc('month', pickup_datetime),
    service_type