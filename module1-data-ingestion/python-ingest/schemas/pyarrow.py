import pyarrow as pa


def green_taxi():
    return {
        'VendorID': pa.int64,
        'lpep_pickup_datetime': pa.date64,
        'lpep_dropoff_datetime': pa.date64,
        'passenger_count': pa.int64,
        'trip_distance': pa.float64,
        'PULocationID': pa.Int64,
        'DOLocationID': pa.Int64,
        'RatecodeID': pa.Int64,
        'store_and_fwd_flag': pa.string,
        'payment_type': pa.Int64,
        'fare_amount': pa.float64,
        'extra': pa.float64,
        'mta_tax': pa.float64,
        'improvement_surcharge': pa.float64,
        'tip_amount': pa.float64,
        'tolls_amount': pa.float64,
        'total_amount': pa.float64,
        'congestion_surcharge': pa.float64,
        'ehail_fee': pa.float64,
        'trip_type': pa.int64,
    }


def yellow_taxi():
    return {
        'VendorID': pa.int64,
        'tpep_pickup_datetime': pa.date64,
        'tpep_dropoff_datetime': pa.date64,
        'passenger_count': pa.int64,
        'trip_distance': pa.float64,
        'PULocationID': pa.int64,
        'DOLocationID': pa.int64,
        'RatecodeID': pa.int64,
        'store_and_fwd_flag': pa.String,
        'payment_type': pa.int64,
        'fare_amount': pa.float64,
        'extra': pa.float64,
        'mta_tax': pa.float64,
        'improvement_surcharge': pa.float64,
        'tip_amount': pa.float64,
        'tolls_amount': pa.float64,
        'total_amount': pa.float64,
        'congestion_surcharge': pa.float64,
    }


def fhv_taxi():
    return {
        'dispatching_base_num': pa.string,
        'pickup_datetime': pa.datetime64,
        'dropOff_datetime': pa.datetime64,
        'PUlocationID': pa.int64,
        'DOlocationID': pa.int64,
        'SR_Flag': pa.string,
        'Affiliated_base_number': pa.string,
    }


def zone_lookup():
    return {
        'LocationID': pa.int64,
        'Borough': pa.string,
        'Zone': pa.string,
        'service_zone': pa.string,
    }
