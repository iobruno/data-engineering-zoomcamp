from os import getenv

from hydra import compose, initialize
from loguru import logger
from sqlalchemy import create_engine, exc, text
from typer import BadParameter, Context, Option, Typer

from app.df_repository import FhvTaxiRepo, GreenTaxiRepo, YellowTaxiRepo, ZoneLookupRepo
from app.processor import (
    FhvProcessor,
    GreenTaxiProcessor,
    YellowTaxiProcessor,
    ZoneLookupProcessor,
    progress,
)

cli = Typer(no_args_is_help=True)


def load_conf():
    with initialize(version_base=None, config_path="..", job_name="pyingest"):
        return compose(config_name="datasets")


def test_db_conn(conn_str: str):
    engine = create_engine(conn_str)
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
            logger.info("Connection successfully established!")
    except exc.OperationalError as ex:
        raise BadParameter(f"You must specify the db credentials with env variables - {ex}")


@cli.callback()
def callback(ctx: Context):
    db_user = getenv("DB_USERNAME")
    db_pass = getenv("DB_PASSWORD")
    db_name = getenv("DB_NAME", "nyc_taxi")
    db_host = getenv("DB_HOST", "localhost")
    db_port = getenv("DB_PORT", 5432)

    conn_string = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    adbc_conn_string = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    logger.info("Attempting to connect to Postgresql with env vars...")
    test_db_conn(conn_string)
    ctx.obj = {"conn_string": conn_string, "adbc_conn_string": adbc_conn_string}


@cli.command(name="ingest", help="CLI app to extract NYC Trips data and load into Postgres")
def ingest_db(
    ctx: Context,
    yellow: bool = Option(False, "--yellow", "-y", help="Fetch Yellow taxi dataset"),
    green: bool = Option(False, "--green", "-g", help="Fetch Green cab dataset"),
    fhv: bool = Option(False, "--fhv", "-f", help="Fetch FHV cab dataset"),
    zones: bool = Option(False, "--zones", "-z", help="Fetch Zone lookup dataset"),
    polars_ff: bool = Option(False, "--use-polars", help="Feature flag to use Polars"),
):
    if not any([yellow, green, fhv, zones]):
        raise BadParameter("You must either specify at least one dataset flag (-z | -y | -g | -f)")

    conn_string = ctx.obj.get("adbc_conn_string") if polars_ff else ctx.obj.get("conn_string")
    logger.info("Loading datasets...")
    datasets = load_conf()
    logger.info("Starting dataset processing...")

    with progress:
        if green:
            endpoints = datasets.green_trip_data
            processor = GreenTaxiProcessor(polars_ff=polars_ff)
            repo = GreenTaxiRepo(conn_string)
            processor.run(endpoints, repo, "replace")

        if yellow:
            endpoints = datasets.yellow_trip_data
            processor = YellowTaxiProcessor(polars_ff=polars_ff)
            repo = YellowTaxiRepo(conn_string)
            processor.run(endpoints, repo, "replace")

        if fhv:
            endpoints = datasets.fhv_trip_data
            processor = FhvProcessor(polars_ff=polars_ff)
            repo = FhvTaxiRepo(conn_string)
            processor.run(endpoints, repo, "replace")

        if zones:
            endpoints = datasets.zone_lookups
            processor = ZoneLookupProcessor(polars_ff=polars_ff)
            repo = ZoneLookupRepo(conn_string)
            processor.run(endpoints, repo, "replace")

    logger.info("All done!")
