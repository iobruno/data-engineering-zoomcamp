if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    return data.rename(columns={
        'VendorID': 'vendor_id',
        'lpep_pickup_datetime': 'lpep_pickup_datetime',
        'lpep_dropoff_datetime': 'lpep_dropoff_datetime',
        'passenger_count': 'passenger_count',
        'trip_distance': 'trip_distance',
        'PULocationID': 'pu_location_id',
        'DOLocationID': 'do_location_id',
        'RatecodeID': 'ratecode_id',
        'store_and_fwd_flag': 'store_and_fwd_flag',
        'payment_type': 'payment_type',
        'fare_amount': 'fare_amount',
        'extra': 'extra',
        'mta_tax': 'mta_tax',
        'improvement_surcharge': 'improvement_surcharge',
        'tip_amount': 'tip_amount',
        'tolls_amount': 'tolls_amount',
        'total_amount': 'total_amount',
        'congestion_surcharge': 'congestion_surcharge',
        'ehail_fee': 'ehail_fee',
        'trip_type': 'trip_type',
    })
