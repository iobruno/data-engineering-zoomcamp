from pathlib import Path
from spark.schemas import rides_schema
from spark.session import cfg_local_spark_session

root_dir = Path(__file__).parent
dataset_dir = root_dir.joinpath("datasets")


if __name__ == "__main__":
    spark = cfg_local_spark_session(name="pyspark-streaming")
    rides_df = spark.read\
        .option("header", True)\
        .schema(rides_schema())\
        .csv(path=str(dataset_dir))

    rides_df.printSchema()
