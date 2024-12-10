from os import getenv
from pathlib import Path

import pandas as pd
from hydra import compose, initialize
from prefect import flow, get_run_logger, task
from prefect_gcp import GcpCredentials, GcsBucket


@task(name="serialize-df-to-gcs")
def upload_from_df(gcs_bucket: GcsBucket, df: pd.DataFrame, to_path: str, serialization_fmt: str):
    return gcs_bucket.upload_from_dataframe(
        df,
        to_path=to_path,
        serialization_format=serialization_fmt,
    )


@task(name="fix-datatypes-for-parquet")
def fix_datatypes_for(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    return df.astype(schema)


@task(name="fetch-dataset", retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


@task(name="prepare-gcs-blocks")
def prepare_gcs_blocks(prefect) -> tuple[GcsBucket, str]:
    logger = get_run_logger()
    gcp_credentials = prefect.gcp_credentials.alias
    lakehouse_raw_block = prefect.gcs.lakehouse_raw

    try:
        logger.info(f"Attempting to load GcsBucket Block '{lakehouse_raw_block.alias}'")
        gcs_bucket = GcsBucket.load(lakehouse_raw_block.alias)
        logger.info("GcsBucket loaded successfully!")
    except (ValueError, RuntimeError):
        logger.warn("GcsBucket Block not found. Working on creating it...")
        logger.info("Fetching GcpCredentials from 'GOOGLE_APPLICATION_CREDENTIALS' env var")
        credentials_file = getenv("GOOGLE_APPLICATION_CREDENTIALS")
        credentials_connector = GcpCredentials(service_account_file=credentials_file)
        credentials_connector.save(gcp_credentials, overwrite=True)
        gcs_bucket = GcsBucket(
            bucket=lakehouse_raw_block.bucket,
            gcp_credentials=credentials_connector,
        )
        gcs_bucket.save(lakehouse_raw_block.alias, overwrite=True)
        logger.info(
            f"GcsBucket {lakehouse_raw_block.alias} created successfully. "
            f"Next runs will use this block instead."
        )

    return gcs_bucket, lakehouse_raw_block.get("blob_prefix", "")


def load_conf():
    with initialize(version_base=None, config_path="../", job_name="csv_to_gcs"):
        return [
            compose(config_name="prefect"),
            compose(config_name="schemas"),
            compose(config_name="datasets"),
        ]


@flow(name="web-csv-to-gcs")
def ingest_csv_to_gcs():
    logger = get_run_logger()
    logger.info("Fetching URL Datasets from .yml")
    prefectcfg, schemas, datasets = load_conf()

    logger.info("Preparing Prefect Block...")
    gcs_bucket, blob_prefix = prepare_gcs_blocks(prefectcfg)

    for dataset, endpoints in datasets.items():
        if endpoints is None:
            logger.info(f"Dataset '{dataset}' contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            expected_blob_name = Path(blob_prefix, dataset, filename)
            raw_df = fetch_csv_from(url=endpoint)
            schema = schemas.get(dataset)

            if schema:
                logger.info(f"{filename} (schema found)")
                cleansed_df = fix_datatypes_for(df=raw_df, schema=schema)
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=cleansed_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="parquet_snappy",
                )
            else:
                logger.warn(f"{filename} (schema not found)")
                blob_name = upload_from_df(
                    gcs_bucket=gcs_bucket,
                    df=raw_df,
                    to_path=str(expected_blob_name),
                    serialization_fmt="csv_gzip",
                )
            logger.info(f"Upload complete: 'gs://{gcs_bucket.bucket}/{blob_name}'")


if __name__ == "__main__":
    ingest_csv_to_gcs()
