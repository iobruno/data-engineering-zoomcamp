import logging
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from omegaconf import OmegaConf
from prefect_gcp import GcpCredentials, GcsBucket

from prefect import flow, task

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%dT%H:%M:%S")

log = logging.getLogger("flow_pg_ingest")


@task(log_prints=True, retries=3)
def load_into_bq_with(df: pd.DataFrame, credentials):
    df.to_gbq(destination_table="dtc_dw_staging.yellow_tripdata",
              project_id="iobruno-data-eng-zoomcamp",
              credentials=credentials.get_credentials_from_service_account(),
              chunksize=500_000,
              if_exists="append")


@task(log_prints=True, retries=3)
def extract_from_gcs(color: str,
                     year_month: str,
                     compression: str = None,
                     local_fs_dir: Path = None) -> pd.DataFrame:
    gcs_bucket = GcsBucket.load("gcs-dtc-datalake-raw")

    if compression == "snappy":
        suffix = ".snappy"
    elif compression == "gzip":
        suffix = ".gz"
    else:
        suffix = ""

    local_fs_dir.mkdir(parents=True, exist_ok=True)

    gcs_path = f"{color}/{color}_tripdata_{year_month}.parquet{suffix}"
    print(f"Fetching: '{gcs_path}'")

    gcs_bucket.get_directory(from_path=gcs_path, local_path=local_fs_dir)
    local_filepath = f"{local_fs_dir}/{gcs_path}"
    return pd.read_parquet(local_filepath)


@flow(name="NYC GCS to BigQuery", log_prints=True)
def ingest():
    try:
        print("Fetching Configurations for GCS to BigQuery ETL from .yml")
        gcs2bq_datasets = cfg.etl.gcs_to_bigquery

        print("Loading up GCP Credentials from Prefect Block...")
        gcp_credentials_block = GcpCredentials.load("prefect-gcs-bigquery-admin-new")

        target_dir: Path = root_dir.joinpath("gcs_datasets")

        for color, year_months in gcs2bq_datasets.items():
            for year_month in year_months:
                df = extract_from_gcs(color=color,
                                      year_month=year_month,
                                      compression="gzip",
                                      local_fs_dir=target_dir)
                print(f"Retrieval successful. Dataframe contains: {len(df)} lines")
                print("Initiating Dataframe transfer to BigQuery...")
                load_into_bq_with(df, credentials=gcp_credentials_block)
                print("Dataframe transfer complete!")

        print("All Done!")

    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
