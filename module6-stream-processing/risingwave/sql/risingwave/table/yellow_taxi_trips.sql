-- See: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
-- Taxicab Technology Service Provider or TPEP

create table if not exists yellow_taxi_trips (
    VendorID bigint,
    tpep_pickup_datetime timestamp,
    tpep_dropoff_datetime timestamp,
    passenger_count numeric,
    trip_distance numeric,
    RatecodeID numeric,
    store_and_fwd_flag string,
    PULocationID bigint,
    DOLocationID bigint,
    payment_type bigint,
    fare_amount numeric,
    extra numeric,
    mta_tax numeric,
    tip_amount numeric,
    tolls_amount numeric,
    improvement_surcharge numeric,
    total_amount numeric,
    congestion_surcharge numeric,
    airport_fee numeric
) with (
    connector='kafka',
    topic='yellow-taxi-tripdata',
    properties.bootstrap.server='broker:29092',
    scan.startup.mode='earliest'
) format plain encode json;