import os
import pandas as pd

from df_persistence import persist_df, persist_df_with, split_df_in_chunks_with
from omegaconf import OmegaConf
from pathlib import Path
from sqlalchemy import create_engine
from typing import List
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
)

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

progress = Progress(
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total}",
    "•",
    "[progress.percentage]{task.percentage:>3.1f}%"
)


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
    filenames = list(map(lambda string: string.split("/")[-1], yellow_trip_data_urls))

    with progress:
        task_ids: List[TaskID] = [progress.add_task(name, start=False, total=0) for name in filenames]

        for idx, url in enumerate(yellow_trip_data_urls):
            df = pd.read_csv(url, engine='pyarrow')
            dfs, qty = split_df_in_chunks_with(df)

            progress.start_task(task_id=task_ids[idx])
            progress.update(task_id=task_ids[idx], completed=0, total=qty)

            for chunk_id, new_df in enumerate(dfs):
                persist_df_with(df=new_df, conn=db_conn, table_name="ntl_yellow_taxi")
                progress.update(task_id=task_ids[idx], completed=chunk_id+1)

            progress.stop_task(task_id=task_ids[idx])


if __name__ == "__main__":
    conn = setup_db_conn()
    conn.connect()
    ingest_yellow_taxi_data_with(db_conn=conn)
    exit(0)
