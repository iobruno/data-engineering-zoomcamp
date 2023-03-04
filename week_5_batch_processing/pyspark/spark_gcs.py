from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType


def read_csv_from_gcs(spark: SparkSession,
                      gcs_prefix: str,
                      view_name: str = None,
                      schema: StructType = None,
                      has_header: bool = True) -> DataFrame:
    if schema:
        sdf = spark.read\
            .option("header", has_header)\
            .schema(schema)\
            .csv(path=gcs_prefix)
    else:
        sdf = spark.read\
            .option("header", has_header)\
            .option("inferSchema", True)\
            .csv(path=gcs_prefix)

    if view_name:
        sdf.createTempView(view_name)

    return sdf


def read_parquet_from_gcs(spark: SparkSession,
                          gcs_prefix: str,
                          view_name: str = None) -> DataFrame:
    sdf: DataFrame = spark.read.parquet(gcs_prefix)
    sdf.createTempView(view_name)
    return sdf
