from os import getenv
from pathlib import Path
from typing import Tuple

import pandas as pd
from hydra import compose, initialize
from prefect_gcp import GcpCredentials, GcsBucket

from prefect import flow, get_run_logger, task


@task(name="serialize-df-to-gcs")
def upload_from_df(gcs_bucket: GcsBucket, df: pd.DataFrame, to_path: str, serialization_fmt: str):
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


@task(name="fix-datatypes-for-parquet")
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(name="fetch-dataset", retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    log = get_run_logger()
    log.info(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


@task(name="prepare-gcs-blocks")
def prepare_gcs_blocks(prefect) -> Tuple[GcsBucket, str]:
    gcp_credentials = prefect.gcp_credentials.alias
    lakehouse_raw_block = prefect.gcs.lakehouse_raw
    log = get_run_logger()

    try:
        log.info(f"Attempting to load GcsBucket Block '{lakehouse_raw_block.alias}'")
        gcs_bucket = GcsBucket.load(lakehouse_raw_block.alias)
        log.info(f"GcsBucket loaded successfully!")
    except (ValueError, RuntimeError):
        log.warn(f"GcsBucket Block not found. Working on creating it...")
        log.info(f"Fetching GcpCredentials from 'GOOGLE_APPLICATION_CREDENTIALS' env var")
        credentials_file = getenv("GOOGLE_APPLICATION_CREDENTIALS")
        credentials_connector = GcpCredentials(service_account_file=credentials_file)
        credentials_connector.save(gcp_credentials, overwrite=True)
        gcs_bucket = GcsBucket(
            bucket=lakehouse_raw_block.bucket, gcp_credentials=credentials_connector
        )
        gcs_bucket.save(lakehouse_raw_block.alias, overwrite=True)
        log.info(
            f"GcsBucket {lakehouse_raw_block.alias} created successfully. "
            f"Next runs will use this block instead."
        )

    return gcs_bucket, lakehouse_raw_block.get("blob_prefix", "")


def load_conf():
    with initialize(version_base=None, config_path="../", job_name="csv_to_gcs"):
        return [
            compose(config_name="prefect"),
            compose(config_name='schemas'),
            compose(config_name='datasets')
        ]


@flow(name="web-csv-to-gcs")
def ingest_csv_to_gcs():
    log = get_run_logger()
    log.info("Fetching URL Datasets from .yml")
    prefectcfg, schemas, datasets = load_conf()

    log.info("Preparing Prefect Block...")
    gcs_bucket, blob_prefix = prepare_gcs_blocks(prefectcfg)

    for dataset, endpoints in datasets.items():
        if endpoints is None:
            log.info(f"Dataset '{dataset}' contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            expected_blob_name = Path(blob_prefix, dataset, filename)
            raw_df = fetch_csv_from(url=endpoint)
            schema = schemas.get(dataset)

            if schema:
                log.info(f"{filename} (schema found)")
                cleansed_df = fix_datatypes_for(df=raw_df, schema=schema)
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=cleansed_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="parquet_snappy",
                )
            else:
                log.warn(f"{filename} (schema not found)")
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=raw_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="csv_gzip",
                )
            log.info(f"Upload complete: 'gs://{gcs_bucket.bucket}/{blob_name}'")


if __name__ == "__main__":
    ingest_csv_to_gcs()
