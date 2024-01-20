SELECT
    -- Revenue Grouping
    pickup_zone                             as revenue_zone,
    DATE_TRUNC('month', pickup_datetime)    as revenue_month,    
    service_type                            as service_type,
    -- Additional Calculations
    COUNT(trip_id)                          as total_monthly_trips,
    ROUND(AVG(passenger_count), 2)          as avg_montly_passenger_count,
    ROUND(AVG(trip_distance), 2)            as avg_montly_trip_distance
FROM 
    {{ ref('dim_yellow_green_trips') }}
GROUP BY 
    pickup_zone,
    date_trunc('month', pickup_datetime), 
    service_type