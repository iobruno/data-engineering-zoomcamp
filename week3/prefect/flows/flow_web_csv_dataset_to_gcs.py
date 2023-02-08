import logging
import pandas as pd
import numpy as np

from math import ceil
from omegaconf import OmegaConf
from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcsBucket
from typing import Tuple

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%dT%H:%M:%S")

log = logging.getLogger("flow_pg_ingest")


@task(log_prints=True, retries=3)
def load_into_gcs_with(bucket_name: str, blob_name: str, fs_path: str):
    gcs_bucket = GcsBucket.load("gcs-dtc-datalake-raw")
    gcs_bucket.upload_from_path(
        from_path=fs_path,
        to_path=blob_name
    )


@task(log_prints=True, retries=3)
def save_to_fs_with(df: pd.DataFrame, label: str) -> Tuple[Path, str]:
    filename = f"{label.split('.')[0]}.parquet.gz"
    file_dir = root_dir.joinpath("datasets")
    file_dir.mkdir(parents=True, exist_ok=True)
    filepath = file_dir.joinpath(filename)
    df.to_parquet(filepath, compression='gzip')
    print(f"Dataset '{label}' contains: {len(df)} lines")
    return filepath, filename


@task(log_prints=True, retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="NYC Taxi Trip data CSV Dataset to GCS", log_prints=True)
def ingest():
    try:
        print("Fetching URL Datasets from .yml")
        datasets = cfg.datasets

        if datasets.fhv:
            for endpoint in datasets.fhv:
                filename = endpoint.split("/")[-1]
                df = fetch_csv_from(url=endpoint)
                filepath, parquet_filename = save_to_fs_with(df=df, label=filename)
                load_into_gcs_with(bucket_name=cfg.gcp.gcs_target_bucket,
                                   blob_name=f"fhv/{parquet_filename}",
                                   fs_path=filepath)

    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
