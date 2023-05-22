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
sdk i spark 3.3.2
```

**3.** Install `Hadoop` version `3.3.5` with:
```shell
sdk i hadoop 3.3.5
```

**4.** Install the project dependencies with:
```shell
poetry install --no-root
```

**5.** Finally, to enable integration with google-cloud-storage as an HDFS-compliant,
- download the `gcs-connector-for-hadoop`:
- and copy binary to $SPARK_HOME/jars

```shell
cd $SPARK_HOME/jars/

wget https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar
```

**6.** (Alternatively) When dealing with AWS, refer to the [hadoop-aws document](https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html)

- **IMPORTANT NOTE**: The hadoop-aws version must match the one used to install hadoop on Step 3. So, for this case, hadoop-aws-3.3.5

```shell
cd $SPARK_HOME/jars/

wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.464/aws-java-sdk-bundle-1.12.464.jar

wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.0/hadoop-aws-3.3.0.jar

wget https://repo1.maven.org/maven2/com/google/guava/guava/31.1-jre/guava-31.1-jre.jar
```

**7.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**8.** Application Running

8.1. Either spin up a Jupyter Lab and explore [pyspark_homework.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_homework.ipynb)
or [pyspark_playground.ipynb](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week5/pyspark/pyspark_playground.ipynb)

8.2. Configure `GOOGLE_APPLICATION_CREDENTIALS` env variable pointing to a .json
Service Account with Read Access to GCS, and run:

```shell
python spark_gcs_to_gcs.py
```

## TODO:
- [X] Set up a Jupyter Playground for PySpark
- [X] Explore the SparkSQL API
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Submit a PySpark job to the Google Dataproc
- [ ] Set up a Standalone Cluster for Spark in [kind](https://kind.sigs.k8s.io/)
- [ ] Submit a PySpark job to the Spark Cluster