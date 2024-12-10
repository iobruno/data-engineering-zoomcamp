from os import getenv
from pathlib import Path

import pandas as pd
from hydra import compose, initialize
from prefect import flow, get_run_logger, task
from prefect_sqlalchemy import SqlAlchemyConnector


def split_df_in_chunks_with(df, chunk_size: int = 1_000_000) -> list[pd.DataFrame]:
    return [
        df.iloc[chunk_id : chunk_id + chunk_size]
        for chunk_id in range(0, len(df), chunk_size)
    ]


@task(name="serialize-df-into-db", retries=3)
def load_db_with(sqlalchemy: SqlAlchemyConnector, df: pd.DataFrame, tbl_name: str, label: str):
    logger = get_run_logger()
    chunks = split_df_in_chunks_with(df)
    num_chunks = len(chunks)
    with sqlalchemy.get_connection(begin=False) as engine:
        for chunk_id, df_chunk in enumerate(chunks):
            logger.info(f"[{label}] Now processing: Chunk {chunk_id+1}/{num_chunks}")
            df_chunk.to_sql(tbl_name, con=engine, if_exists="append", index=False)


@task(name="drop-invalid-entries")
def drop_trips_with_no_passengers(df: pd.DataFrame) -> pd.DataFrame:
    logger = get_run_logger()
    refined_df = df[df["passenger_count"] != 0]
    excluded_entries = df["passenger_count"].isin([0]).sum()
    logger.info(f"Num of entries with zero passengers: {excluded_entries}")
    return refined_df


@task(name="fetch-dataset", retries=3)
def fetch_csv_from(url: str) -> pd.DataFrame:
    logger = get_run_logger()
    logger.info(f"Now fetching: {url}")
    return pd.read_csv(url, engine="pyarrow")


@task(name="prepare-sqlachemy-block")
def prepare_sqlalchemy_block(sqlalchemy) -> SqlAlchemyConnector:
    logger = get_run_logger()
    try:
        logger.info(f"Attempting to load SqlAlchemy Block '{sqlalchemy.alias}'")
        conn_block = SqlAlchemyConnector.load(sqlalchemy.alias)
        logger.info("SqlAlchemy loaded successfully!")
    except ValueError:
        logger.warning("SqlAlchemy Block not found. Working on creating it...")
        user = getenv("DB_USERNAME")
        passwd = getenv("DB_PASSWORD")
        dbname = getenv("DB_NAME", "nyc_taxi")
        host = getenv("DB_HOST", "localhost")
        port = getenv("DB_PORT", 5432)
        conn_block = SqlAlchemyConnector(
            connection_info=f"postgresql+psycopg://{user}:{passwd}@{host}:{port}/{dbname}"
        )
        conn_block.save(sqlalchemy.alias, overwrite=True)

    return conn_block


def load_conf():
    with initialize(version_base=None, config_path="../", job_name="sqlalchemy_ingest"):
        return [
            compose(config_name="prefect"),
            compose(config_name="schemas"),
            compose(config_name="datasets"),
        ]


@flow(name="web-csv-to-sqlalchemy")
def sqlalchemy_ingest():
    logger = get_run_logger()
    logger.info("Fetching URL Datasets from .yaml")
    prefectcfg, schemas, datasets = load_conf()

    logger.info("Preparing Prefect Block...")
    conn_block = prepare_sqlalchemy_block(prefectcfg.sqlalchemy)

    for dataset, endpoints in datasets.items():
        if endpoints is None:
            logger.info(f"Dataset '{dataset}' contains no valid endpoints entries. Skipping...")
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
