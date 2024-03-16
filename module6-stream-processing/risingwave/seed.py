import logging

import pandas as pd
import polars as pl
from confluent_kafka import Producer as KafkaProducer
from sqlalchemy import create_engine, text
from typer import Argument, Option, Typer
from typing_extensions import Annotated

cli = Typer(no_args_is_help=True)
logging.basicConfig()
logging.root.setLevel(logging.INFO)


def stream_records_to_kafka(producer: KafkaProducer, records):
    logging.info("Starting real time updates")
    for i, (_, record) in enumerate(records.iterrows()):
        message = record.to_json()
        producer.produce("trip_data", value=message.encode(), key=None)

        if i % 100_000 == 0:
            logging.info(f"Sent {i} records")
            producer.flush()


def batch_process_records_to_kafka(producer: KafkaProducer, records):
    logging.info("Sending historical data")
    pass


def send_records_to_kafka(kafka_config, dataset_url: str, streaming: bool):
    producer = KafkaProducer(kafka_config)
    records = pd.read_parquet(dataset_url)

    if streaming:
        return stream_records_to_kafka(producer, records)
    return batch_process_records_to_kafka(producer, records)


def send_csv_records(
    endpoint: str,
    tbl_name: str,
    conn_string: str,
    write_disposition: str = "append",
    engine: str = "sqlalchemy",
):
    # Workaround for RisingWave, since 'write_disposition='replace' doesn't work yet
    # Also, Polars' adbc-driver (to use Postgres' COPY mechanism doesn't work either)
    with create_engine(conn_string).connect() as conn:
        conn.execute(text("drop table if exists taxi_zone"))

    df = pl.read_csv(endpoint).rename(mapping={
        "LocationID": "location_id",
        "Borough": "borough",
        "Zone": "zone",
        "service_zone": "service_zone",
    })
    return df.write_database(
        table_name=tbl_name,
        connection=conn_string,
        if_table_exists=write_disposition,
        engine=engine,
    )


@cli.command("seed", help="Populates RisingWave DB with TaxiZone, and Kafka's yellow-trip-data")
def seed(
    bootstrap_server: Annotated[str, Argument(envvar="KAFKA_BOOTSTRAP_SERVERS")],
    rw_host: Annotated[str, Argument(envvar="RISINGWAVE_HOST")] = "localhost",
    rw_port: Annotated[int, Argument(envvar="RISINGWAVE_PORT")] = 4566,
    rw_db: Annotated[str, Argument(envvar="RISINGWAVE_DB")] = "dev",
    rw_user: Annotated[str, Argument(envvar="RISINGWAVE_USER")] = "root",
    rw_pass: Annotated[str, Argument(envvar="RISINGWAVE_PASS")] = "",
    stream_ff: Annotated[bool, Option("--use-streaming")] = True,
):
    # logging.info("Loading taxi zone data to RisingWave...")
    # num_records = send_csv_records(
    #     endpoint="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv",
    #     tbl_name="taxi_zones",
    #     conn_string=f"postgresql://{rw_user}:{rw_pass}@{rw_host}:{rw_port}/{rw_db}",
    # )
    # logging.info(f"Inserted/Overwritten: {num_records} entries for 'taxi_zones'")

    send_records_to_kafka(
        kafka_config={
            "bootstrap.servers": "localhost:9092",
            "queue.buffering.max.messages": 1_000_000,
        },
        dataset_url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet",
        streaming=stream_ff,
    )


if __name__ == "__main__":
    cli()
