import os

from pyspark.sql import SparkSession
from spark_gcs import read_csv_from_gcs


def config_spark_session(name: str, master: str) -> SparkSession:
    spark = SparkSession.builder\
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")\
        .config("spark.driver.memory", "2g")\
        .config("spark.executor.memory", "8g")\
        .config("spark.cores.max", 8)\
        .appName(name)\
        .master(master)\
        .getOrCreate()

    spark._jsc.hadoopConfiguration()\
        .set("google.cloud.auth.service.account.json.keyfile",
             os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    return spark


def join_dataframe_with_spark_sql(spark: SparkSession):
    return spark.sql(""""
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
                service_zone as service_zone                
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


def main():
    spark = config_spark_session(name="pyspark-playground",
                                 master="local[*]")

    read_csv_from_gcs(spark, gcs_prefix="", view_name="fhv")
    read_csv_from_gcs(spark, gcs_prefix="", view_name="zones")

    sdf = join_dataframe_with_spark_sql(spark)
    sdf.printSchema()


if __name__ == "__main__":
    main()
