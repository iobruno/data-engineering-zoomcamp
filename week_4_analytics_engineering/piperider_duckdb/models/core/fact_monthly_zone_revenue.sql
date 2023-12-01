SELECT
    -- Revenue Grouping
    pickup_zone                 as revenue_zone,
    date_trunc('month', pickup_datetime) as revenue_month,    
    service_type,
    -- Revenue Calculations
    SUM(fare_amount)            as revenue_monthly_fare,
    SUM(extra)                  as revenue_monthly_extra,
    SUM(mta_tax)                as revenue_monthly_mta_tax,
    SUM(tip_amount)             as revenue_monthly_tip_amount,
    SUM(tolls_amount)           as revenue_monthly_tolls_amount,
    SUM(ehail_fee)              as revenue_monthly_ehail_fee,
    SUM(improvement_surcharge)  as revenue_monthly_improvement_surcharge,
    SUM(total_amount)           as revenue_monthly_total_amount,
    SUM(congestion_surcharge)   as revenue_monthly_congestion_surcharge,
FROM 
    {{ ref('dim_yellow_green_trips') }}
GROUP BY 
    pickup_zone, 
    date_trunc('month', pickup_datetime), 
    service_type