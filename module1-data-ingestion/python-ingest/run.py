import logging

from omegaconf import OmegaConf
from pathlib import Path
from rich.logging import RichHandler
from rich.progress import *
from typing_extensions import Annotated
from typer import Typer, Argument, Option

from src.dataframe_fetcher import (
    DataframeFetcher,
    PolarsFetcher,
    PandasFetcher,
)

from src.dataframe_repository import (
    SQLRepository,
    GreenTaxiRepository,
    YellowTaxiRepository,
    FhvTaxiRepository,
    ZoneLookupRepository
)


config_file = Path(__file__).parent.joinpath("app.yml")
cfg = OmegaConf.load(config_file)
log = logging.getLogger("sqlalchemy_ingest")
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


def extract_load_with(fetcher: DataframeFetcher, repository: SQLRepository, endpoints: List[str]):
    filenames = [Path(endpoint).stem for endpoint in endpoints]
    tasks = [progress.add_task(name, start=False, total=0) for name in filenames]

    for idx, record in enumerate(fetcher.fetch_all(endpoints)):
        progress.update(task_id=tasks[idx], completed=0, total=len(record.slices))
        progress.start_task(task_id=tasks[idx])
        for chunk_id, _ in enumerate(repository.save_all(record.slices)):
            progress.update(task_id=tasks[idx], completed=chunk_id + 1)


# fmt: off
@cli.command(name="ingest", help="CLI app to extract NYC Trips data and load into Postgres")
def ingest_db(
    db_dialect: Annotated[str, Argument(envvar="DATABASE_DIALECT", hidden=False)],
    db_host: Annotated[str, Argument(envvar="DATABASE_HOST", hidden=True)],
    db_port: Annotated[str, Argument(envvar="DATABASE_PORT", hidden=True)],
    db_name: Annotated[str, Argument(envvar="DATABASE_NAME", hidden=True)],
    db_username: Annotated[str, Argument(envvar="DATABASE_USERNAME", hidden=True,)],
    db_password: Annotated[str, Argument(envvar="DATABASE_PASSWORD", hidden=True,)],
    yellow: Annotated[bool, Option("--yellow", "-y", help="Fetch Yellow taxi dataset")] = False,
    green: Annotated[bool, Option("--green", "-g", help="Fetch Green cab dataset")] = False,
    fhv: Annotated[bool, Option("--fhv", "-f", help="Fetch FHV cab dataset")] = False,
    zones: Annotated[bool, Option("--zones", "-z", help="Fetch Zone lookup dataset")] = False,
):
    # fmt: on
    log.info(f"Connecting to '{db_dialect}' with credentials on ENV VARs...")
    db_settings = db_dialect, db_host, db_port, db_name, db_username, db_password
    with progress:
        green_dataset_endpoints = cfg.datasets.green_trip_data
        yellow_dataset_endpoints = cfg.datasets.yellow_trip_data
        fhv_dataset_endpoints = cfg.datasets.fhv_trip_data
        zone_lookup_dataset_endpoints = cfg.datasets.zone_lookups

        df_fetcher: DataframeFetcher = PolarsFetcher()

        if green and green_dataset_endpoints:
            green_taxi_repo = GreenTaxiRepository.with_config(*db_settings)
            extract_load_with(df_fetcher, green_taxi_repo, green_dataset_endpoints)

        if yellow and yellow_dataset_endpoints:
            yellow_taxi_repo = YellowTaxiRepository.with_config(*db_settings)
            extract_load_with(df_fetcher, yellow_taxi_repo, yellow_dataset_endpoints)

        if fhv and fhv_dataset_endpoints:
            fhv_taxi_repo = FhvTaxiRepository.with_config(*db_settings)
            extract_load_with(df_fetcher, fhv_taxi_repo, fhv_dataset_endpoints)

        if zones and zone_lookup_dataset_endpoints:
            zone_lookup_repo = ZoneLookupRepository.with_config(*db_settings)
            extract_load_with(df_fetcher, zone_lookup_repo, zone_lookup_dataset_endpoints)


if __name__ == "__main__":
    cli()
