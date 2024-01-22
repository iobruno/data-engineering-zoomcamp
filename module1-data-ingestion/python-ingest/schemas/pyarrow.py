import pyarrow as pa


def green_taxi():
    return {
        'VendorID': 'Int64',
        'lpep_pickup_datetime': 'datetime64[s]',
        'lpep_dropoff_datetime': 'datetime64[s]',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'RatecodeID': 'Int64',
        'store_and_fwd_flag': 'string',
        'payment_type': 'Int64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'improvement_surcharge': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'total_amount': 'float64',
        'congestion_surcharge': 'float64',
        'ehail_fee': 'float64',
        'trip_type': 'Int64',
    }


def yellow_taxi():
    return {
        'VendorID': 'Int64',
        'tpep_pickup_datetime': 'datetime64[s]',
        'tpep_dropoff_datetime': 'datetime64[s]',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'RatecodeID': 'Int64',
        'store_and_fwd_flag': 'string',
        'payment_type': 'Int64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'improvement_surcharge': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'total_amount': 'float64',
        'congestion_surcharge': 'float64',
    }


def fhv_taxi():
    return {
        'dispatching_base_num': 'string',
        'pickup_datetime': 'datetime64[s]',
        'dropOff_datetime': 'datetime64[s]',
        'PUlocationID': 'Int64',
        'DOlocationID': 'Int64',
        'SR_Flag': 'string',
        'Affiliated_base_number': 'string',
    }


def zone_lookup():
    return {
        'LocationID': 'Int64',
        'Borough': 'string',
        'Zone': 'string',
        'service_zone': 'string',
    }
