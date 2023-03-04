from os import environ as env

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import *
from spark_gcs import read_csv_from_gcs, read_parquet_from_gcs


def join_dfs_with_spark_api(_fhv: DataFrame, _zones: DataFrame) -> DataFrame:
    fhv = _fhv.select(col("dispatching_base_num"),
                      col("Affiliated_base_number").alias("affiliated_base_num"),
                      col("pickup_datetime"),
                      col("dropOff_datetime").alias("dropoff_datetime"),
                      col("PUlocationID").alias("pickup_location_id"),
                      col("DOlocationID").alias("dropoff_location_id"))

    zones = _zones.select(
        col("LocationID").alias("location_id"),
        col("Borough").alias("borough"),
        col("Zone").alias("zone"), col("service_zone"))

    return fhv.alias("f").join(
        zones.alias("pu"),
        col("f.pickup_location_id") == col("pu.location_id"),
        how="inner").join(zones.alias("do"),
                          col("f.dropoff_location_id") == col("do.location_id"),
                          how="inner").select(col("f.dispatching_base_num"),
                                              col("f.affiliated_base_num"),
                                              col("f.pickup_datetime"),
                                              col("pu.zone").alias("pickup_zone"),
                                              col("pu.service_zone").alias("pickup_service_zone"),
                                              col("f.dropoff_location_id"),
                                              col("do.zone").alias("dropoff_zone"),
                                              col("do.service_zone").alias("dropoff_service_zone"))


def join_dfs_with_spark_sql(spark: SparkSession) -> DataFrame:
    return spark.sql("""
        WITH t_fhv AS (
            SELECT
                dispatching_base_num,
                Affiliated_base_number as affiliated_base_num,
                pickup_datetime,
                dropOff_datetime as dropoff_datetime,
                PUlocationID as pickup_location_id,
                DOlocationID as dropoff_location_id
            FROM fhv
        ),

        t_zones AS (
            SELECT
                LocationID as location_id,
                Borough as borough,
                Zone as zone,
                service_zone
            FROM zones
        )

        SELECT
            f.dispatching_base_num,
            f.affiliated_base_num,

            -- Pickup Location
            f.pickup_datetime,
            pu.zone as pickup_zone,
            pu.service_zone as pickup_service_zone,

            -- Dropoff Location
            f.dropoff_location_id,
            do.zone as dropoff_zone,
            do.service_zone as dropoff_service_zone

        FROM t_fhv f
        INNER JOIN t_zones pu ON f.pickup_location_id  = pu.location_id
        INNER JOIN t_zones do ON f.dropoff_location_id = do.location_id
    """)


def zone_lookup_schema() -> StructType:
    return StructType([
        StructField("LocationID", IntegerType(), True),
        StructField("Borough", StringType(), True),
        StructField("Zone", StringType(), True),
        StructField("service_zone", StringType(), True),
    ])


def config_spark_session(name: str, master: str) -> SparkSession:
    spark = SparkSession.builder \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "8g") \
        .config("spark.cores.max", 8) \
        .appName(name) \
        .master(master) \
        .getOrCreate()

    spark._jsc\
        .hadoopConfiguration() \
        .set("google.cloud.auth.service.account.json.keyfile", env["GOOGLE_APPLICATION_CREDENTIALS"])

    return spark


def main():
    fhv_gcs_path = "gs://iobruno_datalake_raw/dtc_ny_taxi_tripdata/fhv/fhv_tripdata_2019-01.parquet.snappy"
    zone_lookup_gcs_path = "gs://iobruno_datalake_raw/dtc_ny_taxi_tripdata/zone_lookup/taxi_zone_lookup.csv"

    spark = config_spark_session(name="pyspark-playground", master="local[*]")

    fhv: DataFrame = read_parquet_from_gcs(spark, gcs_prefix=fhv_gcs_path, view_name="fhv")

    zones: DataFrame = read_csv_from_gcs(spark, gcs_prefix=zone_lookup_gcs_path, view_name="zones",
                                         schema=zone_lookup_schema())

    # Join DataFrames with SparkSQL
    sdf = join_dfs_with_spark_sql(spark)
    sdf.printSchema()
    sdf.show(5, 100, False)

    # Join DataFrames with Spark API
    sdf2 = join_dfs_with_spark_api(fhv, zones)
    sdf2.printSchema()
    sdf2.show(5, 100, False)


if __name__ == "__main__":
    main()
