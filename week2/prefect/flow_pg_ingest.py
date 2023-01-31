import logging
import os
import pandas as pd
import numpy as np

from math import ceil
from omegaconf import OmegaConf
from pathlib import Path
from sqlalchemy import create_engine
from typing import List, Tuple

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

log = logging.getLogger("postgres_ingest")
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
)


def setup_db_conn():
    db_user = os.getenv("DATABASE_USERNAME")
    db_passwd = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")
    conn_string = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"
    return create_engine(conn_string)


def split_df_in_chunks_with(df: pd.DataFrame, max_chunk_size: int = 100000) -> Tuple[List[pd.DataFrame], int]:
    chunks_qty = ceil(len(df) / max_chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


def persist_df_with(df: pd.DataFrame, conn, table_name: str, if_table_exists='append'):
    df.to_sql(table_name, con=conn, if_exists=if_table_exists, index=False)


def ingest_nyc_trip_data_with(conn, table_name: str, dataset_endpoints: List[str]):
    filenames = list(map(lambda string: string.split("/")[-1], dataset_endpoints))

    for idx, url in enumerate(dataset_endpoints):
        df = pd.read_csv(url, engine='pyarrow')
        dfs, qty = split_df_in_chunks_with(df)

        for chunk_id, new_df in enumerate(dfs):
            persist_df_with(df=new_df, conn=conn, table_name=table_name)


def ingest():
    try:
        log.info("Attempting to connect to Postgres with provided credentials on ENV VARs...")
        conn = setup_db_conn()
        conn.connect()
        log.info("Connection successfully established!")

        log.info("Fetching URL Datasets from .yml")
        datasets = cfg.datasets

        if datasets.yellow_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_yellow_taxi",
                                      dataset_endpoints=datasets.yellow_trip_data)

        if datasets.green_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_green_taxi",
                                      dataset_endpoints=datasets.green_trip_data)

        if datasets.zone_lookups:
            ingest_nyc_trip_data_with(conn, "ntl_lookup_zones",
                                      dataset_endpoints=datasets.zone_lookups)

    except Exception as ex:
        log.error(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
