import logging
from math import ceil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from omegaconf import OmegaConf
from prefect_sqlalchemy import SqlAlchemyConnector

from prefect import flow, task

config_file = Path(__file__).parent.parent.joinpath("app.yml")
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
def load_into_postgres_with(df: pd.DataFrame, table_name: str, label: str):
    dfs, qty = split_df_in_chunks_with(df)

    conn_block = SqlAlchemyConnector.load("postgres-docker")
    with conn_block.get_connection(begin=False) as engine:
        for chunk_id, df_chunk in enumerate(dfs):
            print(f"[{label}] Now saving: Chunk {chunk_id+1}/{qty}")
            df_chunk.to_sql(table_name, con=engine, if_exists='append', index=False)


@task(log_prints=True)
def drop_trips_with_no_passengers(df: pd.DataFrame) -> pd.DataFrame:
    refined_df = df[df['passenger_count'] != 0]
    print(f"Excluded entries with zero passengers: {df['passenger_count'].isin([0]).sum()}")
    return refined_df


@task(log_prints=True, retries=3)
def extract_nyc_trip_data_with(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine='pyarrow')


@flow(name="NYC Trip CSV Dataset to Postgres", log_prints=True)
def ingest():
    try:
        print("Fetching URL Datasets from .yml")
        datasets = cfg.datasets

        if datasets.green_trip_data:
            for endpoint in datasets.green_trip_data:
                filename = endpoint.split("/")[-1]
                df = extract_nyc_trip_data_with(url=endpoint)
                cleansed_df = drop_trips_with_no_passengers(df)
                load_into_postgres_with(df=cleansed_df, table_name="ntl_green_taxi", label=filename)

        if datasets.zone_lookups:
            for endpoint in datasets.zone_lookups:
                filename = endpoint.split("/")[-1]
                df = extract_nyc_trip_data_with(url=endpoint)
                load_into_postgres_with(df=df, table_name="ntl_lookup_zones", label=filename)

    except Exception as ex:
        print(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
