import logging
import os
from pathlib import Path

import click
import math
import numpy as np
import pandas as pd
import sqlalchemy
from pandas import DataFrame
from omegaconf import OmegaConf
from typing import List

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]"
)

log = logging.getLogger("postgres_ingest")


def split_df_in_chunks_with(df: pd.DataFrame, chunk_size: int = 100_000) -> [List[DataFrame], int]:
    chunks_qty = math.ceil(len(df) / chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


def ingest_nyc_trip_data_with(conn, table_name: str, dataset_endpoints: List[str]):
    for idx, url in enumerate(dataset_endpoints):
        df = pd.read_csv(url, engine='pyarrow')
        dfs, qty = split_df_in_chunks_with(df)

        for chunk_id, df_chunk in enumerate(dfs):
            df_chunk.to_sql(table_name, con=conn, if_exists="append", index=False)


def setup_db_conn() -> sqlalchemy.Engine:
    db_user = os.getenv("DATABASE_USERNAME")
    db_passwd = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")
    conn_string = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"
    return sqlalchemy.create_engine(conn_string)


@click.command()
@click.option("--with-yellow-trip-data", "-y", count=True)
@click.option("--with-green-trip-data", "-g", count=True)
@click.option("--with-lookup-zones", "-z", count=True)
def ingest(with_yellow, with_green, with_lookup_zones):
    log.info("Attempting to connect to Postgres with provided credentials on ENV VARs...")
    conn = setup_db_conn()
    conn.connect()
    log.info("Connection successfully established!")

    datasets = cfg.datasets

    if with_yellow:
        if datasets.yellow_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_yellow_taxi", datasets.yellow_trip_data)
            log.info("Done persisting the NYC Yellow Taxi trip data into DB")
        else:
            log.warning("Skipping Yellow trip data. The endpoint list is empty")

    if with_green:
        if datasets.green_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_green_taxi", datasets.green_trip_data)
            log.info("Done persisting the NYC Green Taxi trip data into DB")
        else:
            log.warning("Skipping Green trip data. The endpoint list is empty")

    if with_lookup_zones:
        if datasets.zone_lookups:
            ingest_nyc_trip_data_with(conn, "ntl_lookup_zones", datasets.zone_lookups)
            log.info("Done persisting the NYC Lookup Zones")
        else:
            log.warning("Skipping Lookup zones. The endpoint list is empty")


if __name__ == "__main__":
    ingest()
