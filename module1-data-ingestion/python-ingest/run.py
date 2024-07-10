from pathlib import Path

from hydra import compose, initialize
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from typer import Argument, Option, Typer
from typing_extensions import Annotated
from src.processor import *

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


def gen_progress_tasks_for(endpoints: List[str]):
    filenames = [Path(endpoint).stem for endpoint in endpoints]
    return [
        progress.add_task(name, start=False, total=float("inf"), completed=0) for name in filenames
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

    with progress:
        if green:
            endpoints = cfg.datasets.green_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            processor = GreenTaxiProcessor(polars_ff=polars_ff)
            processor.run(endpoints, db_settings, "replace", tasks, progress)

        if yellow:
            endpoints = cfg.datasets.yellow_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            processor = YellowTaxiProcessor(polars_ff=polars_ff)
            processor.run(endpoints, db_settings, "replace", tasks, progress)

        if fhv:
            endpoints = cfg.datasets.fhv_trip_data
            tasks = gen_progress_tasks_for(endpoints)
            processor = FhvProcessor(polars_ff=polars_ff)
            processor.run(endpoints, db_settings, "replace", tasks, progress)

        if zones:
            endpoints = cfg.datasets.zone_lookups
            tasks = gen_progress_tasks_for(endpoints)
            processor = ZoneLookupProcessor(polars_ff=polars_ff)
            processor.run(endpoints, db_settings, "replace", tasks, progress)


if __name__ == "__main__":
    cli()
