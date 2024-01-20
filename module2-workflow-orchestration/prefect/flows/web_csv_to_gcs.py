import os
from pathlib import Path

import pandas as pd

from omegaconf import DictConfig, OmegaConf
from prefect import flow, task
from prefect_gcp import GcpCredentials, GcsBucket
from pandas import DataFrame


root_dir = Path(__file__).parent.parent

config_file = root_dir.joinpath("app.yml")
schema_file = root_dir.joinpath("schemas.yml")

cfg = OmegaConf.load(config_file)
schemas = OmegaConf.load(schema_file)


@task(log_prints=True)
def upload_from_df(gcs_bucket: GcsBucket, df: DataFrame, to_path: str, serialization_fmt: str):
    """Upload a Pandas DataFrame to Google Cloud Storage in various formats.
    GitHub PR> https://github.com/PrefectHQ/prefect-gcp/pull/140

    This uploads the data in a Pandas DataFrame to GCS in a specified format,
    such as .csv, .csv.gz, .parquet, .snappy.parquet, and .gz.parquet

    Args:
        gcs_bucket: The Prefect GcsBucket Block
        df: The Pandas DataFrame to be uploaded.
        to_path: The destination path for the uploaded DataFrame.
        serialization_fmt: The format to serialize the DataFrame into.
            The valid options are: 'csv', 'csv_gzip', 'parquet', 'parquet_snappy', 'parquet_gz'
            Defaults to `DataFrameSerializationFormat.CSV_GZIP`

    Returns:
        The path that the object was uploaded to.
    """
    return gcs_bucket.upload_from_dataframe(
        df, to_path=to_path, serialization_format=serialization_fmt
    )


@task(log_prints=True)
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


def prepare_gcs_block(prefect) -> (GcsBucket, str):
    gcp_credentials = prefect.gcp_credentials.alias
    lakehouse_raw_block = prefect.gcs.lakehouse_raw

    try:
        print(f"Attempting to load GcsBucket Block '{lakehouse_raw_block.alias}'")
        gcs_bucket = GcsBucket.load(lakehouse_raw_block.alias)
        print(f"GcsBucket loaded successfully!")
    except (ValueError, RuntimeError):
        print(f"GcsBucket Block not found. Working on creating it...")
        print(f"Fetching GcpCredentials from 'GOOGLE_APPLICATION_CREDENTIALS' env var")
        credentials_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        credentials_connector = GcpCredentials(service_account_file=credentials_file)
        credentials_connector.save(gcp_credentials, overwrite=True)
        gcs_bucket = GcsBucket(
            bucket=lakehouse_raw_block.bucket, gcp_credentials=credentials_connector
        )
        gcs_bucket.save(lakehouse_raw_block.alias, overwrite=True)
        print(
            f"GcsBucket {lakehouse_raw_block.alias} created successfully. "
            f"Next runs will use this block instead."
        )

    return gcs_bucket, lakehouse_raw_block.get("blob_prefix", "")


@flow(name="Web CSV Dataset to GCS", log_prints=True)
def ingest_csv_to_gcs():
    print("Fetching URL Datasets from .yml")
    datasets: DictConfig = cfg.datasets

    print("Preparing Prefect Block...")
    gcs_bucket, blob_prefix = prepare_gcs_block(cfg.prefect)

    for dataset, endpoints in datasets.items():
        if endpoints is None:
            print(f"Dataset '{dataset}' contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            expected_blob_name = Path(blob_prefix, dataset, filename)
            raw_df = fetch_csv_from(url=endpoint)
            df_schema = schemas.get(dataset)

            if df_schema:
                cleansed_df = fix_datatypes_for(df=raw_df, schema=df_schema)
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=cleansed_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="parquet_snappy",
                )
            else:
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=raw_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="csv_gzip",
                )
            print(f"Upload complete: 'gs://{gcs_bucket.bucket}/{blob_name}'")


if __name__ == "__main__":
    ingest_csv_to_gcs()
