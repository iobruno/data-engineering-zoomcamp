import logging
from pathlib import Path

import math
import numpy as np
import pandas as pd
import sqlalchemy
import typer
from omegaconf import OmegaConf
from rich.logging import RichHandler
from rich.progress import *
from typing_extensions import Annotated
from typing import Optional

config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)

progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total}",
    "•",
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeElapsedColumn(),
)

app = typer.Typer()
log = logging.getLogger("postgres_ingest")


def split_df_in_chunks_with(df, chunk_size: int = 100_000) -> [List[pd.DataFrame], int]:
    chunks_qty = math.ceil(len(df) / chunk_size)
    return np.array_split(df, chunks_qty), chunks_qty


def ingest_nyc_trip_data_with(conn, table_name: str, dataset_endpoints: List[str]):
    filenames = [Path(endpoint).stem for endpoint in dataset_endpoints]
    task_ids = [progress.add_task(name, start=False, total=0) for name in filenames]

    for idx, url in enumerate(dataset_endpoints):
        df = pd.read_csv(url, engine="pyarrow")
        # Converts dataframe columns to lower case, otherwise, in PostgreSQL
        # all fields that start with uppercase will have to be quoted " for querying
        df.columns = map(str.lower, df.columns)
        dfs, qty = split_df_in_chunks_with(df)
        progress.update(task_id=task_ids[idx], completed=0, total=qty)
        progress.start_task(task_id=task_ids[idx])

        for chunk_id, df_chunk in enumerate(dfs):
            df_chunk.to_sql(table_name, con=conn, if_exists="append", index=False)
            progress.update(task_id=task_ids[idx], completed=chunk_id + 1)

        progress.stop_task(task_id=task_ids[idx])


def setup_db_conn(*db_settings) -> sqlalchemy.Engine:
    (db_driver, db_host, db_port, db_user, db_passwd, db_name) = db_settings

    if db_driver == "mysql":
        conn_prefix = f"mysql+mysqlconnector"
    else:
        conn_prefix = f"postgresql+psycopg"

    conn_string = f"{conn_prefix}://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"
    return sqlalchemy.create_engine(conn_string)


# fmt: off
@app.command(help="CLI app to extract NYC Trips data and load into Postgres")
def ingest(
    db_host: Annotated[str, typer.Argument(
        envvar="DATABASE_HOST", hidden=True
    )],
    db_port: Annotated[str, typer.Argument(
        envvar="DATABASE_PORT", hidden=True
    )],
    db_name: Annotated[str, typer.Argument(
        envvar="DATABASE_NAME", hidden=True
    )],
    db_username: Annotated[str, typer.Argument(
        envvar="DATABASE_USERNAME", hidden=True,
    )],
    db_password: Annotated[str, typer.Argument(
        envvar="DATABASE_PASSWORD", hidden=True,
    )],
    db_driver: Annotated[str, typer.Argument(
        envvar="DATABASE_DRIVER", hidden=False,
    )],
    yellow: Annotated[Optional[bool], typer.Option(
        "--yellow", "-y", help="Fetch datasets from NYC Yellow Trip"
    )] = False,
    green: Annotated[Optional[bool], typer.Option(
        "--green", "-g", help="Fetch datasets from: NYC Green Trip"
    )] = False,
    zones: Annotated[Optional[bool], typer.Option(
        "--zones", "-z", help="Fetch datasets from: Lookup Zones"
    )] = False,
):
    # fmt: on
    log.info(f"Attempting to connect to '{db_driver}' with credentials on ENV VARs...")
    conn = setup_db_conn(db_driver, db_host, db_port, db_username, db_password, db_name)
    conn.connect()
    log.info("Connection successfully established!")

    with progress:
        datasets = cfg.datasets
        if yellow:
            if datasets.yellow_trip_data:
                ingest_nyc_trip_data_with(conn, "ntl_yellow_taxi", datasets.yellow_trip_data)
                log.info("Done persisting the NYC Yellow Taxi trip data into DB")
            else:
                log.warning("Skipping Yellow trip data. The endpoint list is empty")

        if green:
            if datasets.green_trip_data:
                ingest_nyc_trip_data_with(conn, "ntl_green_taxi", datasets.green_trip_data)
                log.info("Done persisting the NYC Green Taxi trip data into DB")
            else:
                log.warning("Skipping Green trip data. The endpoint list is empty")

        if zones:
            if datasets.zone_lookups:
                ingest_nyc_trip_data_with(conn, "ntl_lookup_zones", datasets.zone_lookups)
                log.info("Done persisting the NYC Lookup Zones")
            else:
                log.warning("Skipping Lookup zones. The endpoint list is empty")


if __name__ == "__main__":
    typer.run(ingest)
