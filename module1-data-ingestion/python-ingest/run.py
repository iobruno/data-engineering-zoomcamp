import logging
from pathlib import Path
from typing import List

from omegaconf import OmegaConf
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from typer import Argument, Option, Typer
from typing_extensions import Annotated

import schemas.polars as pl_schema
import schemas.pyarrow as pa_schema
import schemas.renaming_strategy as rename
from src.dataframe_fetcher import (
    DataframeFetcher,
    PandasFetcher,
    PolarsFetcher,
)
from src.dataframe_repository import (
    FhvTaxiRepository,
    GreenTaxiRepository,
    SQLRepository,
    YellowTaxiRepository,
    ZoneLookupRepository,
)

root_folder = Path(__file__).parent
dataset = OmegaConf.load(root_folder.joinpath("datasets.yml"))
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
    repo.save(df_slice, if_table_exists=write_disposition)
    progress.update(task_id=tid, completed=completeness, total=total_parts)

    for _ in repo.save_all(other_slices):
        completeness += 1
        progress.update(task_id=tid, completed=completeness, total=total_parts)

    extract_load_with(fetcher, repo, remain_endpoints, remain_tasks, if_table_exists="append")


# fmt: off
@cli.command(name="ingest", help="CLI app to extract NYC Trips data and load into Postgres")
def ingest_db(
    db_name: Annotated[str, Argument(envvar="DATABASE_NAME", hidden=True)],
    db_username: Annotated[str, Argument(envvar="DATABASE_USERNAME", hidden=True,)],
    db_password: Annotated[str, Argument(envvar="DATABASE_PASSWORD", hidden=True,)],
    db_host: Annotated[str, Argument(envvar="DATABASE_HOST", hidden=True)],
    db_port: Annotated[str, Argument(envvar="DATABASE_PORT", hidden=True)] = 5432,
    yellow: Annotated[bool, Option("--yellow", "-y", help="Fetch Yellow taxi dataset")] = False,
    green: Annotated[bool, Option("--green", "-g", help="Fetch Green cab dataset")] = False,
    fhv: Annotated[bool, Option("--fhv", "-f", help="Fetch FHV cab dataset")] = False,
    zones: Annotated[bool, Option("--zones", "-z", help="Fetch Zone lookup dataset")] = False,
    polars_ff: Annotated[bool, Option("--use-polars", help="Feature flag to enable Polars")] = False
):
    # fmt: on
    log.info("Connecting to 'postgres' with credentials on ENV VARs...")
    db_settings = db_host, db_port, db_name, db_username, db_password
    with progress:
        green_dataset_endpoints = dataset.green_trip_data
        yellow_dataset_endpoints = dataset.yellow_trip_data
        fhv_dataset_endpoints = dataset.fhv_trip_data
        zones_dataset_endpoints = dataset.zone_lookups
        df_fetcher: DataframeFetcher

        if polars_ff:
            schema_ref = pl_schema
            df_fetcher = PolarsFetcher()
            log.info("Using 'polars' as Dataframe library")
        else:
            schema_ref = pa_schema
            df_fetcher = PandasFetcher()
            log.info("Using 'pandas' as Dataframe library")

        def gen_progress_tasks_for(endpoints: List[str]):
            filenames = [Path(endpoint).stem for endpoint in endpoints]
            return [
                progress.add_task(name, start=False, total=float('inf'), completed=0)
                for name in filenames
            ]

        if green and green_dataset_endpoints:
            green_repo = GreenTaxiRepository.with_config(*db_settings)
            green_tasks = gen_progress_tasks_for(green_dataset_endpoints)
            fetcher = df_fetcher\
                .with_schema(schema_ref.green_taxi())\
                .with_renaming_strategy(rename.green_taxi())
            extract_load_with(fetcher, green_repo, green_dataset_endpoints, green_tasks)

        if yellow and yellow_dataset_endpoints:
            yellow_repo = YellowTaxiRepository.with_config(*db_settings)
            yellow_tasks = gen_progress_tasks_for(yellow_dataset_endpoints)
            fetcher = df_fetcher\
                .with_schema(schema_ref.yellow_taxi())\
                .with_renaming_strategy(rename.yellow_taxi())
            extract_load_with(fetcher, yellow_repo, yellow_dataset_endpoints, yellow_tasks)

        if fhv and fhv_dataset_endpoints:
            fhv_repo = FhvTaxiRepository.with_config(*db_settings)
            fhv_tasks = gen_progress_tasks_for(fhv_dataset_endpoints)
            fetcher = df_fetcher\
                .with_schema(schema_ref.fhv_taxi())\
                .with_renaming_strategy(rename.fhv_taxi())
            extract_load_with(fetcher, fhv_repo, fhv_dataset_endpoints, fhv_tasks)

        if zones and zones_dataset_endpoints:
            zone_repo = ZoneLookupRepository.with_config(*db_settings)
            zone_tasks = gen_progress_tasks_for(zones_dataset_endpoints)
            fetcher = df_fetcher\
                .with_schema(schema_ref.zone_lookup())\
                .with_renaming_strategy(rename.zone_lookup())
            extract_load_with(fetcher, zone_repo, zones_dataset_endpoints, zone_tasks)


if __name__ == "__main__":
    cli()
