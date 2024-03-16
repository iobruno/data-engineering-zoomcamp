import json
import logging
import math
import time

import polars as pl
from confluent_kafka import Producer as KafkaProducer
from sqlalchemy import create_engine, text
from typer import Argument, Option, Typer
from typing_extensions import Annotated

cli = Typer(no_args_is_help=True)
logging.basicConfig()
logging.root.setLevel(logging.INFO)


def acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))


def push_to_kafka(producer: KafkaProducer, topic: str, records, chunk_size: int, delay: float = 0):
    num_chunks = math.ceil(len(records) / chunk_size)
    total_records = 0
    for chunk_id in range(num_chunks):
        chunk = records.slice(offset=chunk_id * chunk_size, length=chunk_size)
        real_chk_size = len(chunk)
        total_records += real_chk_size
        for row in chunk.iter_rows(named=True):
            message = json.dumps(row, default=str).encode("utf-8")
            producer.produce(topic, key="", value=message, callback=acked)

        producer.flush()
        logging.info(f"Sent {real_chk_size} messages (Total: {total_records})")
        time.sleep(delay)


def send_records_to_kafka(kafka_config, topic: str, dataset_url: str, streaming: bool):
    producer = KafkaProducer(kafka_config)
    records = pl.read_parquet(dataset_url)

    # TODO: Updates pickup and dropoff times to simulate rides happening now
    

    if streaming:
        logging.info("Starting real time updates to Kafka")
        return push_to_kafka(producer, topic, records, chunk_size=500, delay=5)

    logging.info("Sending historical data to Kafka")
    return push_to_kafka(producer, topic, records, chunk_size=500_000)


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

    df = pl.read_csv(endpoint).rename(
        mapping={
            "LocationID": "location_id",
            "Borough": "borough",
            "Zone": "zone",
            "service_zone": "service_zone",
        }
    )
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
    stream_ff: Annotated[bool, Option("--use-streaming")] = False,
):
    logging.info("Loading taxi zone data to RisingWave...")
    num_records = send_csv_records(
        endpoint="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv",
        tbl_name="taxi_zones",
        conn_string=f"postgresql://{rw_user}:{rw_pass}@{rw_host}:{rw_port}/{rw_db}",
    )
    logging.info(f"Inserted/Overwritten: {num_records} entries for 'taxi_zones'")

    send_records_to_kafka(
        kafka_config={
            "bootstrap.servers": "localhost:9092",
            "client.id": "rising-wave-seed",
            "queue.buffering.max.messages": 1_000_000,
        },
        topic="yellow-taxi-tripdata",
        dataset_url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet",
        streaming=stream_ff,
    )


if __name__ == "__main__":
    cli()
