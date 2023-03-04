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
- Python 3.9 / 3.10
- JDK 11 / 17
- PySpark (Python API for Spark)
- Spark SQL
- Jupyter Notebook
- [Poetry](https://python-poetry.org/docs/)

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

**6.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**7.** Application Running

6.1. Either spin up a Jupyter Lab and explore [pyspark_homework.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_homework.ipynb)
or [pyspark_playground.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_playground.ipynb)

6.2. Configure `GOOGLE_APPLICATION_CREDENTIALS` env variable pointing to a .json
Service Account with Read Access to GCS, and run:

```shell
python spark_app.py
```

## TODO:
- [X] Set up a Jupyter Playground for PySpark
- [X] Explore the SparkSQL API
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Set up a Standalone Cluster for Spark
- [ ] Submit a PySpark job to the Cluster
