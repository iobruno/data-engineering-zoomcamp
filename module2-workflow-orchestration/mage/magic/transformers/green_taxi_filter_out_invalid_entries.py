if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    zero_passenger_trips = data['passenger_count'].isin([0]).sum()
    zero_distance_trips = data['trip_distance'].isin([0]).sum()
    print(f"Records with zero passengers: {zero_passenger_trips}")
    print(f"Records with zero trip_distance: {zero_distance_trips}")
    return data[
        (data['passenger_count'] > 0) &
        (data['trip_distance'] > 0)
    ]
