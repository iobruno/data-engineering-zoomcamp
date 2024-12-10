import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import GcsFileSystem

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    bucket_name = 'iobruno-lakehouse-raw'
    blob_prefix = 'nyc_tlc_dataset/green_taxi_data'
    root_path = f"{bucket_name}/{blob_prefix}"

    data['pickup_date'] = data['lpep_pickup_datetime'].dt.date
    table = pa.Table.from_pandas(data)

    pq.write_to_dataset(
        table,
        partition_cols=['pickup_date'],
        root_path=root_path,
        filesystem=GcsFileSystem(),
        compression='snappy',
        basename_template='green-taxi-data-part-{i}.snappy.parquet'
    )
