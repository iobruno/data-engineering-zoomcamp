from pyspark.sql import SparkSession


def cfg_local_spark_session(name: str, master: str = "local[*]") -> SparkSession:
    spark = SparkSession.builder \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "8g") \
        .config("spark.cores.max", 8) \
        .appName(name) \
        .master(master) \
        .getOrCreate()

    return spark
