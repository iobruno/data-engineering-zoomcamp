import os
from pathlib import Path

import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect_gcp import GcpCredentials, GcsBucket

from prefect import flow, task

root_dir = Path(__file__).parent.parent

config_file = root_dir.joinpath("app.yml")
schema_file = root_dir.joinpath("schemas.yml")

cfg = OmegaConf.load(config_file)
schemas = OmegaConf.load(schema_file)


@task(log_prints=True)
def upload_from_dataframe(
        gcs_bucket: GcsBucket,
        pandas_df: pd.DataFrame,
        to_path: str,
        serialization_format: str
):
    """Upload a Pandas DataFrame to Google Cloud Storage in various formats.
    GitHub PR> https://github.com/PrefectHQ/prefect-gcp/pull/140

    This function uploads the data in a Pandas DataFrame to Google Cloud Storage
    in a specified format, such as .csv, .csv.gz, .parquet, .snappy.parquet, and .gz.parquet

    Args:
        gcs_bucket: The Prefect GcsBucket Block
        pandas_df: The Pandas DataFrame to be uploaded.
        to_path: The destination path for the uploaded DataFrame.
        serialization_format: The format to serialize the DataFrame into.
            The valid options are: 'csv', 'csv_gzip', 'parquet', 'parquet_snappy', 'parquet_gz'
            Defaults to `DataFrameSerializationFormat.CSV_GZIP`

    Returns:
        The path that the object was uploaded to.
    """
    gcs_bucket.upload_from_dataframe(
        df=pandas_df, to_path=to_path, serialization_format=serialization_format
    )


@task(log_prints=True)
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


def prepare_gcs_block(prefect) -> (GcsBucket, str):
    gcp_credentials_config = prefect.gcp_credentials
    gcp_credentials_alias = gcp_credentials_config.get("gcs_bigquery")
    gcs_block_config = prefect.gcs.get("dtc_datalake_raw")

    try:
        print(f"Attempting to load GcsBucket Block '{gcs_block_config.alias}'")
        gcs_bucket = GcsBucket.load(gcs_block_config.alias)
        print(f"GcsBucket loaded successfully!")
    except (ValueError, RuntimeError):
        print(f"GcsBucket Block not found. Working on creating it...")
        print(f"Fetching GcpCredentials from 'GOOGLE_APPLICATION_CREDENTIALS' env var")
        credentials_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        credentials_connector = GcpCredentials(service_account_file=credentials_file)
        credentials_connector.save(gcp_credentials_alias, overwrite=True)
        gcs_bucket = GcsBucket(bucket=gcs_block_config.bucket,
                               gcp_credentials=credentials_connector)
        gcs_bucket.save(gcs_block_config.alias, overwrite=True)
        print(
            f"GcsBucket {gcs_block_config.alias} created successfully. "
            f"Next runs will use this block instead."
        )

    return gcs_bucket, gcs_block_config.get("blob_prefix", "")


@flow(name="Web CSV Dataset to GCS", log_prints=True)
def ingest_csv_to_gcs():
    print("Fetching URL Datasets from .yml")
    datasets: DictConfig = cfg.datasets
    prefect = cfg.prefect_block

    print("Preparing Prefect Block...")
    gcs_bucket, blob_prefix = prepare_gcs_block(prefect)

    for dataset_name, endpoints in datasets.items():
        if endpoints is None:
            print(
                f"Dataset '{dataset_name}' found in config file, "
                f"but it contains no valid endpoints entries. Skipping..."
            )
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            gcs_path = Path(blob_prefix, dataset_name, filename)
            raw_df = fetch_csv_from(url=endpoint)
            df_schema = schemas.get(dataset_name)

            if df_schema:
                cleansed_df = fix_datatypes_for(df=raw_df, schema=df_schema)
                upload_from_dataframe(
                    gcs_bucket=gcs_bucket,
                    pandas_df=cleansed_df,
                    to_path=str(gcs_path),
                    serialization_format='parquet_snappy'
                )
            else:
                upload_from_dataframe(
                    gcs_bucket=gcs_bucket,
                    pandas_df=raw_df,
                    to_path=str(gcs_path),
                    serialization_format='csv_gzip'
                )


if __name__ == "__main__":
    ingest_csv_to_gcs()