{{ config(
    schema=env_var('DBT_REDSHIFT_SCHEMA')
) }}

select
    -- Revenue Grouping
    pickup_zone                                  as zone,
    service_type                                 as service_type,
    {{ date_trunc("month", "pickup_datetime") }} as order_year,
    -- Revenue Calculations
    round(sum(fare_amount), 2)                   as monthly_fare,
    round(sum(extra), 2)                         as monthly_extra,
    round(sum(mta_tax), 2)                       as monthly_mta_tax,
    round(sum(tip_amount), 2)                    as monthly_tip_amount,
    round(sum(tolls_amount), 2)                  as monthly_tolls_amount,
    round(sum(ehail_fee), 2)                     as monthly_ehail_fee,
    round(sum(improvement_surcharge), 2)         as monthly_improvement_surcharge,
    round(sum(total_amount), 2)                  as monthly_total_amount,
    round(sum(congestion_surcharge), 2)          as monthly_congestion_surcharge
from 
    {{ ref('dim_yellow_green_trips') }}
group by 
    pickup_zone, 
    service_type,
    {{ date_trunc("month", "pickup_datetime") }}
