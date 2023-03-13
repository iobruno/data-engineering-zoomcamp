{{ config(materialize='table')}}

SELECT
    -- Revenue Grouping
    pickup_zone as revenue_zone,
    date_trunc('month', pickup_datetime) as revenue_month,    
    service_type,

    -- Revenue Calculations
    SUM(fare_amount)            AS revenue_monthly_fare,
    SUM(extra)                  AS revenue_monthly_extra,
    SUM(mta_tax)                AS revenue_monthly_mta_tax,
    SUM(tip_amount)             AS revenue_monthly_tip_amount,
    SUM(tolls_amount)           AS revenue_monthly_tolls_amount,
    SUM(ehail_fee)              AS revenue_monthly_ehail_fee,
    SUM(improvement_surcharge)  AS revenue_monthly_improvement_surcharge,
    SUM(total_amount)           AS revenue_monthly_total_amount,
    SUM(congestion_surcharge)   AS revenue_monthly_congestion_surcharge,

FROM {{ ref('fact_yellow_green_trips') }}
GROUP BY 1, 2, 3