def green_taxi():
    return {
        "VendorID": "vendor_id",
        "lpep_pickup_datetime": "lpep_pickup_datetime",
        "lpep_dropoff_datetime": "lpep_dropoff_datetime",
        "passenger_count": "passenger_count",
        "trip_distance": "trip_distance",
        "PULocationID": "pu_location_id",
        "DOLocationID": "do_location_id",
        "RatecodeID": "ratecode_id",
        "store_and_fwd_flag": "store_and_fwd_flag",
        "payment_type": "payment_type",
        "fare_amount": "fare_amount",
        "extra": "extra",
        "mta_tax": "mta_tax",
        "improvement_surcharge": "improvement_surcharge",
        "tip_amount": "tip_amount",
        "tolls_amount": "tolls_amount",
        "total_amount": "total_amount",
        "congestion_surcharge": "congestion_surcharge",
        "ehail_fee": "ehail_fee",
        "trip_type": "trip_type",
    }


def yellow_taxi():
    return {
        "VendorID": "vendor_id",
        "tpep_pickup_datetime": "tpep_pickup_datetime",
        "tpep_dropoff_datetime": "tpep_dropoff_datetime",
        "passenger_count": "passenger_count",
        "trip_distance": "trip_distance",
        "PULocationID": "pu_location_id",
        "DOLocationID": "do_location_id",
        "RatecodeID": "ratecode_id",
        "store_and_fwd_flag": "store_and_fwd_flag",
        "payment_type": "payment_type",
        "fare_amount": "fare_amount",
        "extra": "extra",
        "mta_tax": "mta_tax",
        "improvement_surcharge": "improvement_surcharge",
        "tip_amount": "tip_amount",
        "tolls_amount": "tolls_amount",
        "total_amount": "total_amount",
        "congestion_surcharge": "congestion_surcharge",
    }


def fhv_taxi():
    return {
        "dispatching_base_num": "dispatching_base_num",
        "pickup_datetime": "pickup_datetime",
        "dropOff_datetime": "dropoff_datetime",
        "PUlocationID": "pu_location_id",
        "DOlocationID": "do_location_id",
        "SR_Flag": "sr_flag",
        "Affiliated_base_number": "affiliated_base_number",
    }


def zone_lookup():
    return {
        "LocationID": "location_id",
        "Borough": "borough",
        "Zone": "zone",
        "service_zone": "service_zone",
    }
