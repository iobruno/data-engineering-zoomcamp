import logging
import os
from pathlib import Path
from typing import List

import click
import pandas as pd
from df_persistence import persist_df_with, split_df_in_chunks_with
from omegaconf import OmegaConf
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from sqlalchemy import create_engine

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]",
                    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)])

progress = Progress(TextColumn("[bold blue]{task.description}",
                               justify="left"), BarColumn(), "Chunk: {task.completed}/{task.total}",
                    "•", "[progress.percentage]{task.percentage:>3.1f}%", "•", TimeElapsedColumn())

log = logging.getLogger("postgres_ingest")


def setup_db_conn():
    db_user = os.getenv("DATABASE_USERNAME")
    db_passwd = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")
    conn_string = f"postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"
    return create_engine(conn_string)


def ingest_nyc_trip_data_with(conn, table_name: str, dataset_endpoints: List[str]):
    filenames = list(map(lambda string: string.split("/")[-1], dataset_endpoints))
    task_ids: List[int] = [progress.add_task(name, start=False, total=0) for name in filenames]

    for idx, url in enumerate(dataset_endpoints):
        df = pd.read_csv(url, engine='pyarrow')
        dfs, qty = split_df_in_chunks_with(df)

        progress.start_task(task_id=task_ids[idx])
        progress.update(task_id=task_ids[idx], completed=0, total=qty)

        for chunk_id, new_df in enumerate(dfs):
            persist_df_with(df=new_df, conn=conn, table_name=table_name)
            progress.update(task_id=task_ids[idx], completed=chunk_id + 1)

        progress.stop_task(task_id=task_ids[idx])


@click.command(help="CLI app to extract NYC Trips data and load into Postgres")
@click.option("--with-yellow-trip-data", "-y", count=True,
              help="Enables fetching for: 'NYC Yellow Trip' dataset")
@click.option("--with-green-trip-data", "-g", count=True,
              help="Enables fetching for: 'NYC Green Trip' dataset")
@click.option("--with-lookup-zones", "-z", count=True,
              help="Enables fetching for: 'Lookup Zones' dataset")
def ingest(with_yellow_trip_data, with_green_trip_data, with_lookup_zones):
    log.info("Attempting to connect to Postgres with provided credentials on ENV VARs...")
    conn = setup_db_conn()
    conn.connect()
    log.info("Connection successfully established!")

    datasets = cfg.datasets

    with progress:
        if with_yellow_trip_data:
            if datasets.yellow_trip_data:
                ingest_nyc_trip_data_with(conn, "ntl_yellow_taxi", datasets.yellow_trip_data)
                log.info("Done persisting the NYC Yellow Taxi trip data into DB")
            else:
                log.warning("The Yellow trip data init flag was specified, "
                            "but the endpoint list for 'yellow_trip_data' is empty. Skipping...")

        if with_green_trip_data:
            if datasets.green_trip_data:
                ingest_nyc_trip_data_with(conn, "ntl_green_taxi", datasets.green_trip_data)
                log.info("Done persisting the NYC Green Taxi trip data into DB")
            else:
                log.warning("The Green trip data init flag was specified, "
                            "but the endpoint list for 'green_trip_data' is empty. Skipping...")

        if with_lookup_zones:
            if datasets.zone_lookups:
                ingest_nyc_trip_data_with(conn, "ntl_lookup_zones", datasets.zone_lookups)
                log.info("Done persisting the NYC Lookup Zones")

            else:
                log.warning("The Green trip data init flag was specified, "
                            "but the endpoints list for 'zone_lookups' is empty. Skipping...")

    exit(0)


if __name__ == "__main__":
    ingest()
