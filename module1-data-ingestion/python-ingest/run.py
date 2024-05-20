import logging
from pathlib import Path

from hydra import compose, initialize
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from typer import Argument, Option, Typer
from typing_extensions import Annotated

import schemas.polars as polars_schema
import schemas.pyarrow as pyarrow_schema
import schemas.renaming_strategy as rename
from src.dataframe_fetcher import *
from src.dataframe_repository import *

log = logging.getLogger("py_ingest")

cli = Typer(no_args_is_help=True)

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


def extract_load_with(
        fetcher: DataframeFetcher,
        repo: SQLRepository,
        endpoints: List[str],
        tasks: List[int],
        write_disposition: str = "replace",
):
    if not endpoints:
        return

    endpoint, *remain_endpoints = endpoints
    tid, *remain_tasks = tasks

    record = fetcher.fetch(endpoint)
    df_slice, *other_slices = record.slices
    completeness, total_parts = 1, len(record.slices)

    progress.update(task_id=tid, completed=0, total=total_parts)
    progress.start_task(task_id=tid)

    # This is required since, in 'append' mode, polars.df does not create
    # the table if it doesn't exist. It also guarantees idempotency
    repo.save(df_slice, write_disposition=write_disposition)
    progress.update(task_id=tid, completed=completeness, total=total_parts)

    for _ in repo.save_all(other_slices):
        completeness += 1
        progress.update(task_id=tid, completed=completeness, total=total_parts)

    extract_load_with(fetcher, repo, remain_endpoints, remain_tasks, write_disposition="append")


def green_taxi_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks):
    fetcher = df_fetcher \
        .with_schema(schema_ref.green_taxi()) \
        .with_renaming_strategy(rename.green_taxi())
    repo = GreenTaxiRepository.with_config(*db_settings)
    extract_load_with(fetcher, repo, endpoints, tasks)


def yellow_taxi_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks):
    fetcher = df_fetcher \
        .with_schema(schema_ref.yellow_taxi()) \
        .with_renaming_strategy(rename.yellow_taxi())
    repo = YellowTaxiRepository.with_config(*db_settings)
    extract_load_with(fetcher, repo, endpoints, tasks)


def fhv_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks):
    fetcher = df_fetcher \
        .with_schema(schema_ref.fhv_taxi()) \
        .with_renaming_strategy(rename.fhv_taxi())
    repo = FhvTaxiRepository.with_config(*db_settings)
    extract_load_with(fetcher, repo, endpoints, tasks)


def taxi_zones_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks):
    fetcher = df_fetcher \
        .with_schema(schema_ref.zone_lookup()) \
        .with_renaming_strategy(rename.zone_lookup())
    repo = ZoneLookupRepository.with_config(*db_settings)
    extract_load_with(fetcher, repo, endpoints, tasks)


def gen_progress_tasks_for(endpoints: List[str]):
    filenames = [Path(endpoint).stem for endpoint in endpoints]
    return [
        progress.add_task(name, start=False, total=float("inf"), completed=0)
        for name in filenames
    ]


def load_conf():
    with initialize(version_base=None, config_path=".", job_name="py-ingest"):
        return compose(config_name="datasets")


@cli.command(name="ingest", help="CLI app to extract NYC Trips data and load into Postgres")
def ingest_db(
        db_name: Annotated[str, Argument(envvar="DATABASE_NAME", hidden=True)],
        db_username: Annotated[str, Argument(envvar="DATABASE_USERNAME", hidden=True)],
        db_password: Annotated[str, Argument(envvar="DATABASE_PASSWORD", hidden=True)],
        db_host: Annotated[str, Argument(envvar="DATABASE_HOST", hidden=True)],
        db_port: Annotated[str, Argument(envvar="DATABASE_PORT", hidden=True)] = 5432,
        yellow: Annotated[bool, Option("--yellow", "-y", help="Fetch Yellow taxi dataset")] = False,
        green: Annotated[bool, Option("--green", "-g", help="Fetch Green cab dataset")] = False,
        fhv: Annotated[bool, Option("--fhv", "-f", help="Fetch FHV cab dataset")] = False,
        zones: Annotated[bool, Option("--zones", "-z", help="Fetch Zone lookup dataset")] = False,
        polars_ff: Annotated[bool, Option("--use-polars", help="Feature flag to use Polars")] = False,
):
    log.info("Connecting to 'postgres' with credentials on ENV VARs...")
    db_settings = db_host, db_port, db_name, db_username, db_password
    cfg = load_conf()

    if polars_ff:
        schema_ref = polars_schema
        df_fetcher = PolarsFetcher()
        log.info("Using 'polars' as Dataframe library")
    else:
        schema_ref = pyarrow_schema
        df_fetcher = PandasFetcher()
        log.info("Using 'pandas' as Dataframe library")

    with progress:
        if green:
            endpoints = cfg.datasets.green_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            green_taxi_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks)
        if yellow:
            endpoints = cfg.datasets.yellow_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            yellow_taxi_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks)
        if fhv:
            endpoints = cfg.datasets.fhv_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            fhv_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks)
        if zones:
            endpoints = cfg.datasets.zone_lookups
            tasks = gen_progress_tasks_for(endpoints)
            taxi_zones_processor(endpoints, db_settings, df_fetcher, schema_ref, tasks)


if __name__ == "__main__":
    cli()
