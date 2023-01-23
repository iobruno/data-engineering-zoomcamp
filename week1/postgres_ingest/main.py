import os

from dataset_downloader import load_csv_from
from df_persistence import persist_df

from omegaconf import OmegaConf
from pathlib import Path
from sqlalchemy import create_engine
from typing import List


config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)


def setup_db_conn():
    db_user = os.getenv("DATABASE_USERNAME")
    db_passwd = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")
    conn_string = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"
    return create_engine(conn_string)


def ingest_yellow_taxi_data_with(db_conn):
    yellow_trip_data_urls: List[str] = cfg.datasets.yellow_trip_data

    for url in yellow_trip_data_urls:
        print(f"Now Fetching: '{url}'...")
        df = load_csv_from(url=url)
        persist_df(df=df, conn=db_conn, table_name="ntl_yellow_taxi")


if __name__ == "__main__":
    conn = setup_db_conn()
    conn.connect()
    ingest_yellow_taxi_data_with(db_conn=conn)
