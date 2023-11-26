import logging
import math
import os
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect_sqlalchemy import ConnectionComponents, SqlAlchemyConnector, SyncDriver

from prefect import flow, task

config_file = Path(__file__).parent.parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%dT%H:%M:%S",
)

log = logging.getLogger("flow_pg_ingest")


def split_df_in_chunks_with(
    df: pd.DataFrame, chunk_size: int = 100_000
) -> (List[pd.DataFrame], int):
    chunks_qty = math.ceil(len(df) / chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


@task(log_prints=True, retries=3)
def load_db_with(
    sqlalchemy: SqlAlchemyConnector, pandas_df: pd.DataFrame, tbl_name: str, label: str
):
    dfs, qty = split_df_in_chunks_with(pandas_df)
    with sqlalchemy.get_connection(begin=False) as engine:
        for chunk_id, df_chunk in enumerate(dfs):
            print(f"[{label}] Now saving: Chunk {chunk_id+1}/{qty}")
            df_chunk.to_sql(tbl_name, con=engine, if_exists="append", index=False)


@task(log_prints=True)
def drop_trips_with_no_passengers(df: pd.DataFrame) -> pd.DataFrame:
    refined_df = df[df["passenger_count"] != 0]
    excluded_entries = df["passenger_count"].isin([0]).sum()
    print(f"Excluded entries with zero passengers: {excluded_entries}")
    return refined_df


@task(log_prints=True, retries=3)
def extract_nyc_trip_data_with(url: str) -> pd.DataFrame:
    print(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


@task(log_prints=True)
def prepare_sqlalchemy_block(sqlalchemy: DictConfig) -> SqlAlchemyConnector:
    """
    This attempts to load SqlAlchemy Prefect Block configured for Postgres
    with the name defined in app.yml under the key prefect_block.sqlalchemy.ny_taxi.alias

    If it fails to fetch such block, it will attempt to create one
    using the 'database' defined in the app.yml under the same key.

    As for the 'hostname', 'port', 'username' and 'password',
    They'll be set from the env variables, respectively: DATABASE_HOST,
    DATABASE_PORT, DATABASE_USERNAME and DATABASE_PASSWORD

    :param sqlalchemy: DictConfig with keys for alias, database, hostname, and port
    :return: SqlAlchemyConnector
    """
    try:
        print(f"Attempting to load SqlAlchemy Block '{sqlalchemy.alias}'")
        conn_block = SqlAlchemyConnector.load(sqlalchemy.alias)
        print(f"SqlAlchemy loaded successfully!")
    except ValueError:
        print(f"SqlAlchemy Block not found. Working on creating it...")
        conn_block = SqlAlchemyConnector(
            connection_info=ConnectionComponents(
                driver=SyncDriver.POSTGRESQL_PSYCOPG2,
                database=sqlalchemy.get("database"),
                host=os.environ["DATABASE_HOST"],
                port=os.environ["DATABASE_PORT"],
                username=os.environ["DATABASE_USERNAME"],
                password=os.environ["DATABASE_PASSWORD"],
            )
        )
        conn_block.save(sqlalchemy.alias, overwrite=True)

    return conn_block


@flow(name="NYC Trip CSV Dataset to Postgres", log_prints=True)
def sqlalchemy_ingest():
    print("Fetching URL Datasets from .yml")
    datasets: DictConfig = cfg.datasets
    sqlalchemy: DictConfig = cfg.prefect.sqlalchemy.nyc_taxi

    print("Preparing Prefect Block...")
    conn_block = prepare_sqlalchemy_block(sqlalchemy)

    for endpoint in datasets.green:
        filename = Path(endpoint).name
        df = extract_nyc_trip_data_with(url=endpoint)
        cleansed_df = drop_trips_with_no_passengers(df)
        load_db_with(
            sqlalchemy=conn_block,
            pandas_df=cleansed_df,
            tbl_name="ntl_green_taxi",
            label=filename,
        )

    for endpoint in datasets.zone_lookup:
        filename = Path(endpoint).name
        df = extract_nyc_trip_data_with(url=endpoint)
        load_db_with(
            sqlalchemy=conn_block,
            pandas_df=df,
            tbl_name="ntl_lookup_zones",
            label=filename,
        )


if __name__ == "__main__":
    sqlalchemy_ingest()
