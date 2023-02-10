import io
from pathlib import Path
from typing import Optional

import pandas as pd
from omegaconf import OmegaConf
from prefect_gcp import GcsBucket

from prefect import flow, task

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
cfg = OmegaConf.load(config_file)


@task(log_prints=True, retries=3)
def load_into_gcs_with(bucket_name: str, blob_name: str, fs_path: str):
    gcs_bucket = GcsBucket.load("gcs-dtc-datalake-raw")
    gcs_bucket.upload_from_path(
        from_path=fs_path,
        to_path=blob_name
    )


@task(log_prints=True)
def upload_df_to_gcs(prefect_gcs_block_name: str, blob_name: str, df: pd.DataFrame,
                     output_format: str, compression: Optional[str] = None):
    """
    Upload a pandas Dataframe to Google Cloud Storage as:
        .csv, .csv.gz, .parquet, .parquet.snappy, .parquet.gz

    Args:
    - prefect_gcs_block_name (str): Prefect GCS Bucket name
    - blob_name (str): the actual full blob name (e.g.: /path/to/gcs/blob.csv)
    - df (pd.DataFrame): pandas Dataframe object
    - output_format (str): Specify whether the output should be 'csv' or 'parquet'
    - compression (Optional[str], optional): Specify the compression type for the output.
                                              'csv' supports 'None' or 'gzip', while
                                              'parquet' supports 'None', 'snappy' or 'gzip'.
                                              Defaults to None.

    Returns:
    None
    """
    byte_buffer = io.BytesIO()
    content_type: str = "application/octet-stream"

    if not blob_name.endswith(output_format):
        blob_name = f"{blob_name}.{output_format}"

    if output_format == "csv":
        df.to_csv(path_or_buf=byte_buffer, compression=compression, index=False)
        if compression:
            blob_name = f"{blob_name}.gz"
        else:
            content_type = "text/csv"

    elif output_format == "parquet":
        df.to_parquet(path=byte_buffer, compression=compression, index=False)
        if compression == "gzip":
            blob_name = f"{blob_name}.gz"
        elif compression == "snappy":
            blob_name = f"{blob_name}.snappy"

    else:
        raise RuntimeError("Unsupported output format. Use either 'csv' or 'parquet'")

    byte_buffer.seek(0)
    gcs_bucket = GcsBucket.load(prefect_gcs_block_name)
    gcs_bucket.upload_from_file_object(
        from_file_object=byte_buffer,
        to_path=blob_name,
        content_type=content_type
    )


@task(log_prints=True, retries=3)
def fix_datatypes_for(df: pd.DataFrame) -> pd.DataFrame:
    return df.astype({
        'PUlocationID': 'Int64',
        'DOlocationID': 'Int64',
        'SR_Flag': 'Int64'
    })


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="NYC FHV Trip Data CSV Dataset to GCS", log_prints=True)
def ingest():
    try:
        print("Fetching URL Datasets from .yml")
        datasets = cfg.datasets
        if datasets.fhv:
            for endpoint in datasets.fhv:
                filename = endpoint.split("/")[-1].split(".")[0]
                df = fetch_csv_from(url=endpoint)
                cleansed_df = fix_datatypes_for(df=df)
                upload_df_to_gcs(prefect_gcs_block_name="gcs-dtc-datalake-raw",
                                 blob_name=f"testing_fhv/{filename}",
                                 df=cleansed_df,
                                 output_format='parquet',
                                 compression='gzip')
    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
