import polars as pl


def green_taxi():
    return {
        'VendorID': pl.Int32,
        'lpep_pickup_datetime': pl.Datetime,
        'lpep_dropoff_datetime': pl.Datetime,
        'passenger_count': pl.Int8,
        'trip_distance': pl.Float64,
        'PULocationID': pl.Int32,
        'DOLocationID': pl.Int32,
        'RatecodeID': pl.Int8,
        'store_and_fwd_flag': pl.String,
        'payment_type': pl.Int8,
        'fare_amount': pl.Float64,
        'extra': pl.Float64,
        'mta_tax': pl.Float64,
        'improvement_surcharge': pl.Float64,
        'tip_amount': pl.Float64,
        'tolls_amount': pl.Float64,
        'total_amount': pl.Float64,
        'congestion_surcharge': pl.Float64,
        'ehail_fee': pl.Float64,
        'trip_type': pl.Int8,
    }


def yellow_taxi():
    return {
        'VendorID': pl.Int32,
        'tpep_pickup_datetime': pl.Datetime,
        'tpep_dropoff_datetime': pl.Datetime,
        'passenger_count': pl.Int8,
        'trip_distance': pl.Float64,
        'PULocationID': pl.Int32,
        'DOLocationID': pl.Int32,
        'RatecodeID': pl.Int8,
        'store_and_fwd_flag': pl.String,
        'payment_type': pl.Int8,
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
        'PUlocationID': pl.Int32,
        'DOlocationID': pl.Int32,
        'SR_Flag': pl.String,
        'Affiliated_base_number': pl.String,
    }


def zone_lookup():
    return {
        'LocationID': pl.Int32,
        'Borough': pl.String,
        'Zone': pl.String,
        'service_zone': pl.String,
    }
