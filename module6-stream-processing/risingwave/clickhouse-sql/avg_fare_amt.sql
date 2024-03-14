CREATE TABLE avg_fare_amt(
    avg_fare_amount_per_hour numeric,
    num_rides_per_hour Int64,
) ENGINE = ReplacingMergeTree
PRIMARY KEY (avg_fare_amount_per_hour, num_rides_per_hour);