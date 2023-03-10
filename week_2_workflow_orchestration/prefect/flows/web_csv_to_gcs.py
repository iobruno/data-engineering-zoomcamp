from pathlib import Path

import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect_gcp import GcsBucket

from prefect import flow, task

root_dir = Path(__file__).parent.parent

config_file = root_dir.joinpath("app.yml")
schema_file = root_dir.joinpath("schemas.yml")

cfg = OmegaConf.load(config_file)
schemas = OmegaConf.load(schema_file)


@task(log_prints=True)
def upload_from_dataframe(prefect_gcs_block: str, pandas_df: pd.DataFrame, to_path: str,
                          serialization_fmt: str):
    """Upload a Pandas DataFrame to Google Cloud Storage in various formats.
    GitHub PR> https://github.com/PrefectHQ/prefect-gcp/pull/140

    This function uploads the data in a Pandas DataFrame to Google Cloud Storage
    in a specified format, such as .csv, .csv.gz, .parquet, .parquet.snappy, and .parquet.gz

    Args:
        prefect_gcs_block: The Prefect GcsBlock name
        pandas_df: The Pandas DataFrame to be uploaded.
        to_path: The destination path for the uploaded DataFrame.
        serialization_fmt: The format to serialize the DataFrame into.
            The valid options are: 'csv', 'csv_gzip', 'parquet', 'parquet_snappy', 'parquet_gz'
            Defaults to `OutputFormat.CSV_GZIP`. .

    Returns:
        The path that the object was uploaded to.
    """
    gcs_bucket = GcsBucket.load(prefect_gcs_block)
    gcs_bucket.upload_from_dataframe(df=pandas_df, to_path=to_path,
                                     serialization_format=serialization_fmt)


@task(log_prints=True)
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="Web CSV Dataset to GCS", log_prints=True)
def ingest_csv_to_gcs():
    print("Fetching URL Datasets from .yml")
    datasets: DictConfig = cfg.datasets
    prefect: DictConfig = cfg.prefect

    for dataset_name, endpoints in datasets.items():
        if endpoints is None:
            print(f"Dataset '{dataset_name}' found in config file, "
                  f"but it contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            gcs_path = f"{prefect.gcs_blob_prefix}/{dataset_name}/{filename}"

            raw_df = fetch_csv_from(url=endpoint)
            cleansed_df = fix_datatypes_for(df=raw_df, schema=schemas.get(dataset_name))
            upload_from_dataframe(prefect_gcs_block=prefect.gcs_block_name, pandas_df=cleansed_df,
                                  to_path=gcs_path, serialization_fmt='parquet_snappy')


if __name__ == "__main__":
    ingest_csv_to_gcs()
