create table avg_fare_amount(
    avg_fare_amount_per_hour numeric,
    num_rides_per_hour Int64,
) engine = ReplacingMergeTree
primary key (
    avg_fare_amount_per_hour, 
    num_rides_per_hour
);