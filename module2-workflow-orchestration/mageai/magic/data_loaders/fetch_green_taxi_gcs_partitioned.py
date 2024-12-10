import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import GcsFileSystem

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    bucket_name = 'iobruno-lakehouse-raw'
    blob_prefix = 'nyc_tlc_dataset/green_taxi_data'
    root_path = f"{bucket_name}/{blob_prefix}"
    
    pa_table = pq.read_table(
        source=root_path,
        filesystem=GcsFileSystem(),        
    )

    return pa_table.to_pandas()
