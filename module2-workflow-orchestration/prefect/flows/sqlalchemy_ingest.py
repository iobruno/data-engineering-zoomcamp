import math
from os import getenv
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from hydra import compose, initialize
from prefect_sqlalchemy import SqlAlchemyConnector

from prefect import flow, get_run_logger, task


def split_df_in_chunks_with(df, chunk_size: int = 1_000_000) -> Tuple[List[pd.DataFrame], int]:
    chunks_qty = math.ceil(len(df) / chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


@task(name="serialize-df-into-db", retries=3)
def load_db_with(sqlalchemy: SqlAlchemyConnector, df: pd.DataFrame, tbl_name: str, label: str):
    log = get_run_logger()
    chunks, qty = split_df_in_chunks_with(df)
    with sqlalchemy.get_connection(begin=False) as engine:
        for chunk_id, df_chunk in enumerate(chunks):
            log.info(f"[{label}] Now saving: Chunk {chunk_id+1}/{qty}")
            df_chunk.to_sql(tbl_name, con=engine, if_exists="append", index=False)


@task(name="drop-invalid-entries")
def drop_trips_with_no_passengers(df: pd.DataFrame) -> pd.DataFrame:
    log = get_run_logger()
    refined_df = df[df["passenger_count"] != 0]
    excluded_entries = df["passenger_count"].isin([0]).sum()
    log.info(f"Excluded entries with zero passengers: {excluded_entries}")
    return refined_df


@task(name="fetch-dataset", retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    log = get_run_logger()
    log.info(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


@task(name="prepare-sqlachemy-block")
def prepare_sqlalchemy_block(sqlalchemy) -> SqlAlchemyConnector:
    log = get_run_logger()
    try:
        log.info(f"Attempting to load SqlAlchemy Block '{sqlalchemy.alias}'")
        conn_block = SqlAlchemyConnector.load(sqlalchemy.alias)
        log.info(f"SqlAlchemy loaded successfully!")
    except ValueError:
        log.warning(f"SqlAlchemy Block not found. Working on creating it...")
        user = getenv("DATABASE_USERNAME")
        passwd = getenv("DATABASE_PASSWORD")
        host = getenv("DATABASE_HOST")
        port = getenv("DATABASE_PORT", 5432)
        dbname = getenv("DATABASE_NAME")
        conn_block = SqlAlchemyConnector(
            connection_info=f"postgresql+psycopg://{user}:{passwd}@{host}:{port}/{dbname}"
        )
        conn_block.save(sqlalchemy.alias, overwrite=True)

    return conn_block


def load_conf():
    with initialize(version_base=None, config_path="../", job_name="py-ingest"):
        return compose(config_name="app")


@flow(name="web-csv-to-sqlalchemy")
def sqlalchemy_ingest():
    log = get_run_logger()
    log.info("Fetching URL Datasets from .yaml")
    cfg = load_conf()

    prefect_cfg = cfg.prefect
    datasets = cfg.datasets

    log.info("Preparing Prefect Block...")
    conn_block = prepare_sqlalchemy_block(prefect_cfg.sqlalchemy)

    for dataset, endpoints in datasets.items():
        if endpoints is None:
            log.info(f"Dataset '{dataset}' contains no valid endpoints entries. Skipping...")
            endpoints = []

        for endpoint in endpoints:
            filename = Path(endpoint).name
            df = fetch_csv_from(url=endpoint)

            if dataset in {"yellow", "green"}:
                persisting_df = drop_trips_with_no_passengers(df)
            else:
                persisting_df = df

            load_db_with(
                sqlalchemy=conn_block,
                df=persisting_df,
                tbl_name=dataset,
                label=filename,
            )


if __name__ == "__main__":
    sqlalchemy_ingest()
