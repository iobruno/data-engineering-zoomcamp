# Spark for Batch Processing Pipelines

```
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.3.2
      /_/

spark-sql>
```

This subproject builds `pyspark` playground to develop Batch Processing Pipeline Playground for `NY Taxi Tripdata Datasets`

## Tech Stack
- PySpark (Python API for Spark)
- SparkSQL
- JDK 17 (or JDK 11) 
- Jupyter Notebook (EDA)
- Poetry (to manage python dependencies)


## Up and Running

### Developer Setup

**1.** Install `JDK` 11 or 17. You can do so easily with [SDKMAN!](https://sdkman.io/):

```shell
sdk i java 17.0.6-librca
```

**2.** Install `Spark` version `3.3.x` with:

```shell
sdk i spark 3.3.1
```

**3.** Install `Hadoop` version `3.3.0` with: 
```shell
sdk i hadoop 3.3.0
```

**4.** Install the project dependencies with:
```shell
poetry install --no-root
```

**5.** Finally, to enable integration with google-cloud-storage as an HDFS-compliant,  
- download the `gcs-connector-for-hadoop`:
- and copy binary to $SPARK_HOME/jars

```shell
wget https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar
```
```
cp gcs-connector-latest-hadoop2.jar $SPARK_HOME/jars/
```

**6.** Application Running

6.1. Either spin up a Jupyter Lab and explore [pyspark_homework.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_homework.ipynb) 
or [pyspark_playground.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_playground.ipynb)

6.2. Configure `GOOGLE_APPLICATION_CREDENTIALS` env variable pointing to a .json Service Account with Read Access to GCS

## TODO:
- [X] Set up a Jupyter Playground for PySpark
- [X] Explore the SparkSQL API
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Set up a Standalone Cluster for Spark
- [ ] Submit a PySpark job to the Cluster
