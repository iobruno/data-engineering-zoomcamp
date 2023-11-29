# pySpark Playground

![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776AB.svg?style=flat&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/pySpark-FDEE21?style=flat-square&logo=apachespark&logoColor=orange)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

PySpark Playground for NY Taxi Tripdata Batch Processing Pipeline

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.0
      /_/

Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.9)
Type in expressions to have them evaluated.
Type :help for more information.
```


## Tech Stack
- PySpark with SparkSQL
- Jupyter
- [PDM](https://pdm-project.org/latest/#installation)


## Up and Running

### Developer Setup

**1.** Install `JDK` 11 or 17. You can do so easily with [SDKMAN!](https://sdkman.io/):

```shell
sdk i java 17.0.9-librca
```

**2.** Install `Spark` version `3.5.x` with:

```shell
sdk i spark 3.5.0
```

**3.** Install `Hadoop` version `3.3.5` with:
```shell
sdk i hadoop 3.3.5
```

**4.** Install the project dependencies with:
```shell
pdm sync
```

**5.** Finally, to enable integration with google-cloud-storage as an HDFS-compliant,
- Download and copy the `gcs-connector-for-hadoop` binary to $SPARK_HOME/jars

```shell
cd $SPARK_HOME/jars/ && \
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
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Code format/lint with Ruff
- [X] Set up a Jupyter Playground for PySpark
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Submit a PySpark job to the Google Dataproc
- [ ] Deploy [Spark to Kubernetes with Helm](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) using: [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/)
- [ ] Submit a PySpark job to the K8s Spark Cluster