from pathlib import Path
from spark.schemas import rides_schema
from spark.session import cfg_local_spark_session
from omegaconf import OmegaConf
from pyspark.sql.functions import to_json, struct

root_dir = Path(__file__).parent
dataset_dir = root_dir.joinpath("datasets")

cfg = OmegaConf.load(root_dir.joinpath("app.yml"))


if __name__ == "__main__":
    kafka_cfg = cfg.kafka
    spark = cfg_local_spark_session(name="pyspark-streaming")

    rides_df = spark.read\
        .option("header", True)\
        .schema(rides_schema())\
        .csv(path=str(dataset_dir))

    rides_df.selectExpr(
        "CAST(pickup_location_id AS STRING) AS key",
        "to_json(struct(*)) AS value"
    )\
        .write\
        .format("kafka")\
        .option("topic", "pyspark")\
        .option("kafka.bootstrap.servers", kafka_cfg.bootstrap_servers)\
        .save()
