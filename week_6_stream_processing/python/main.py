from pyspark.sql import SparkSession
from pathlib import Path
from pyspark_schema import rides_schema


root_dir = Path(__file__).parent
dataset_dir = root_dir.joinpath("datasets")


def config_spark_session(name: str, master: str = "local[*]") -> SparkSession:
    spark = SparkSession.builder \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "8g") \
            .config("spark.cores.max", 8) \
            .appName(name) \
            .master(master) \
            .getOrCreate()

    return spark


if __name__ == "__main__":
    spark = config_spark_session(name="pyspark-streaming")
    rides_df = spark.read\
        .option("header", True)\
        .schema(rides_schema())\
        .csv(path=str(dataset_dir))

    rides_df.printSchema()
