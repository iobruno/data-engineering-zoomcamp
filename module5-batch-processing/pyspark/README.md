# PySpark Playground

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![PySpark](https://img.shields.io/badge/pySpark-3.5-E36B22?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=3C3A3E)
![Jupyter](https://img.shields.io/badge/Jupyter-31393F.svg?style=flat&logo=jupyter&logoColor=F37726&labelColor=31393F)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

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
- [PySpark with SparkSQL](https://spark.apache.org/docs/latest/api/python/user_guide)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


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