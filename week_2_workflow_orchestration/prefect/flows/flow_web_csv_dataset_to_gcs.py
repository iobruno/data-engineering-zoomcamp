import logging
from math import ceil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from omegaconf import OmegaConf
from prefect_gcp import GcsBucket

from prefect import flow, task

root_dir = Path(__file__).parent.parent
config_file = root_dir.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%dT%H:%M:%S")

log = logging.getLogger("flow_pg_ingest")


def split_df_in_chunks_with(df: pd.DataFrame,
                            max_chunk_size: int = 100000) -> Tuple[List[pd.DataFrame], int]:
    chunks_qty = ceil(len(df) / max_chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


@task(log_prints=True, retries=3)
def load_into_gcs_with(bucket_name: str, blob_name: str, fs_path: str):
    gcs_bucket = GcsBucket.load("gcs-dtc-datalake-raw")
    gcs_bucket.upload_from_path(from_path=fs_path, to_path=blob_name)


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

        if datasets.green_trip_data:
            for endpoint in datasets.green_trip_data:
                filename = endpoint.split("/")[-1]
                df = fetch_csv_from(url=endpoint)
                filepath, parquet_filename = save_to_fs_with(df=df, label=filename)
                load_into_gcs_with(bucket_name=cfg.gcp.gcs_target_bucket,
                                   blob_name=f"green/{parquet_filename}",
                                   fs_path=filepath)

        if datasets.yellow_trip_data:
            for endpoint in datasets.yellow_trip_data:
                filename = endpoint.split("/")[-1]
                df = fetch_csv_from(url=endpoint)
                filepath, parquet_filename = save_to_fs_with(df=df, label=filename)
                load_into_gcs_with(bucket_name=cfg.gcp.gcs_target_bucket,
                                   blob_name=f"yellow/{parquet_filename}",
                                   fs_path=filepath)

    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
