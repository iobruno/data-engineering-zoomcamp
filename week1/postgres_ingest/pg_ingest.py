import click
import logging
import os
import pandas as pd

from df_persistence import persist_df_with, split_df_in_chunks_with
from omegaconf import OmegaConf
from pathlib import Path
from sqlalchemy import create_engine
from typing import List
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeElapsedColumn

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

log = logging.getLogger("postgres_ingest")
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)

progress = Progress(
    TextColumn("[bold blue]{task.description}", justify="left"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total}",
    "•",
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeElapsedColumn()
)


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
    task_ids: List[TaskID] = [
        progress.add_task(name, start=False, total=0)
        for name in filenames
    ]

    for idx, url in enumerate(dataset_endpoints):
        df = pd.read_csv(url, engine='pyarrow')
        dfs, qty = split_df_in_chunks_with(df)

        progress.start_task(task_id=task_ids[idx])
        progress.update(task_id=task_ids[idx], completed=0, total=qty)

        for chunk_id, new_df in enumerate(dfs):
            persist_df_with(df=new_df, conn=conn, table_name=table_name)
            progress.update(task_id=task_ids[idx], completed=chunk_id+1)

        progress.stop_task(task_id=task_ids[idx])


def parse_args_and_compute_datasets(conn, datasets, with_yellow_trip_data, with_green_trip_data, with_lookup_zones):
    if with_yellow_trip_data:
        if datasets.yellow_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_yellow_taxi", dataset_endpoints=datasets.yellow_trip_data)
            log.info("Done persisting the NYC Yellow Taxi trip data into DB")
        else:
            log.warning("The Yellow trip data init flag was specified, but the endpoint list for"
                        "'yellow_trip_data' is empty.\nSkipping...")
    if with_green_trip_data:
        if datasets.green_trip_data:
            ingest_nyc_trip_data_with(conn, "ntl_green_taxi", dataset_endpoints=datasets.green_trip_data)
            log.info("Done persisting the NYC Green Taxi trip data into DB")
        else:
            log.warning("The Green trip data init flag was specified, but the endpoint list for"
                        "'green_trip_data' is empty.\nSkipping...")
    if with_lookup_zones:
        if datasets.zone_lookups:
            ingest_nyc_trip_data_with(conn, "ntl_lookup_zones", dataset_endpoints=datasets.zone_lookups)
            log.info("Done persisting the NYC Lookup Zones")

        else:
            log.warning("The Green trip data init flag was specified, but the endpoints list for"
                        "'zone_lookups' is empty.\nSkipping...")


@click.command()
@click.option("--with-yellow-trip-data", "-y", count=True)
@click.option("--with-green-trip-data", "-g", count=True)
@click.option("--with-lookup-zones", "-z", count=True)
def ingest(with_yellow_trip_data, with_green_trip_data, with_lookup_zones):
    try:
        log.info("Attempting to connect to Postgres with provided credentials on ENV VARs...")
        conn = setup_db_conn()
        conn.connect()
        log.info("Connection successfully established!")

        with progress:
            datasets = cfg.datasets
            parse_args_and_compute_datasets(conn=conn, datasets=datasets,
                                            with_yellow_trip_data=with_yellow_trip_data,
                                            with_green_trip_data=with_green_trip_data,
                                            with_lookup_zones=with_lookup_zones)
        exit(0)

    except Exception as ex:
        log.error(ex)
        exit(-1)


if __name__ == "__main__":
    ingest()
