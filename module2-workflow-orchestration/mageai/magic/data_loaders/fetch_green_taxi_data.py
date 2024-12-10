import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


green_taxi_schema = {
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

@data_loader
def load_data_from_api(*args, **kwargs):
    urls = [
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz",
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz",
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz"
    ]

    green_taxi_dataset = [pd.read_csv(url, engine='pyarrow', dtype=green_taxi_schema) for url in urls]
    return pd.concat(green_taxi_dataset)