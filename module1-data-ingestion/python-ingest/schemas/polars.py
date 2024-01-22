import polars as pl


def green_taxi():
    return {
        'VendorID': pl.Int64,
        'lpep_pickup_datetime': pl.String,
        'lpep_dropoff_datetime': pl.String,
        'passenger_count': pl.Int64,
        'trip_distance': pl.Float64,
        'PULocationID': pl.Int64,
        'DOLocationID': pl.Int64,
        'RatecodeID': pl.Int64,
        'store_and_fwd_flag': pl.String,
        'payment_type': pl.Int64,
        'fare_amount': pl.Float64,
        'extra': pl.Float64,
        'mta_tax': pl.Float64,
        'improvement_surcharge': pl.Float64,
        'tip_amount': pl.Float64,
        'tolls_amount': pl.Float64,
        'total_amount': pl.Float64,
        'congestion_surcharge': pl.Float64,
        'ehail_fee': pl.Float64,
        'trip_type': pl.Int64,
    }


def yellow_taxi():
    return {
        'VendorID': pl.Int64,
        'tpep_pickup_datetime': pl.String,
        'tpep_dropoff_datetime': pl.String,
        'passenger_count': pl.Int64,
        'trip_distance': pl.Float64,
        'PULocationID': pl.Int64,
        'DOLocationID': pl.Int64,
        'RatecodeID': pl.Int64,
        'store_and_fwd_flag': pl.String,
        'payment_type': pl.Int64,
        'fare_amount': pl.Float64,
        'extra': pl.Float64,
        'mta_tax': pl.Float64,
        'improvement_surcharge': pl.Float64,
        'tip_amount': pl.Float64,
        'tolls_amount': pl.Float64,
        'total_amount': pl.Float64,
        'congestion_surcharge': pl.Float64,
    }


def fhv_taxi():
    return {
        'dispatching_base_num': pl.String,
        'pickup_datetime': pl.String,
        'dropOff_datetime': pl.String,
        'PUlocationID': pl.Int64,
        'DOlocationID': pl.Int64,
        'SR_Flag': pl.String,
        'Affiliated_base_number': pl.String,
    }


def zone_lookup():
    return {
        'LocationID': pl.Int64,
        'Borough': pl.String,
        'Zone': pl.String,
        'service_zone': pl.String,
    }