{{ config(materialize='table')}}

SELECT
    -- Revenue Grouping
    pickup_zone AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,    
    service_type,

    -- Additional Calculations
    COUNT(trip_id)        AS total_monthly_trips,
    AVG(passenger_count)  AS avg_montly_passenger_count,
    AVG(trip_distance)    AS avg_montly_trip_distance

FROM {{ ref('fact_yellow_green_trips') }}
GROUP BY 1, 2, 3