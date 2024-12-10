# Batch processing with PySpark

![Python](https://img.shields.io/badge/Python-3.11_|_3.10-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![PySpark](https://img.shields.io/badge/pySpark-3.5-E36B22?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=3C3A3E)
![Jupyter](https://img.shields.io/badge/Jupyter-31393F.svg?style=flat&logo=jupyter&logoColor=F37726&labelColor=31393F)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

PySpark Playground for NY Taxi Tripdata Batch Processing Pipeline

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.3
      /_/

Using Python version 3.11.9 (main, Jun  6 2024 18:26:44)
Spark context Web UI available at http://192.168.15.29:4040
Spark context available as 'sc' (master = local[*], app id = local-1724831152309).
SparkSession available as 'spark'.
```

## Tech Stack
- [PySpark](https://spark.apache.org/docs/latest/api/python/user_guide)
- [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Docker](https://docs.docker.com/get-docker/)

## Up and Running

### Developer Setup

**1.** Install `JDK` 11 or 17, Spark 3.5.x, and Hadoop:
```shell
sdk i java 17.0.13-librca
sdk i spark 3.5.3
sdk i hadoop 3.4.1
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
uv sync
```

**3.** Activate the virtualenv created by `uv`:
```shell
source .venv/bin/activate
```

**4. (Optional)**  Install pre-commit:
```shell
brew install pre-commit
```

From root folder where `.pre-commit-config.yaml` is located, run:
```shell
pre-commit install
```

**5.** Spin up the Spark Cluster
```shell
docker compose -f ../docker-compose.yml up -d
```

## TODO:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Code format/lint with Ruff
- [X] Set up a Jupyter Playground for PySpark
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Enable Spark to read from AWS S3
- [ ] Submit a PySpark job to the Google Dataproc
- [ ] Deploy [Spark to Kubernetes with Helm](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) with [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/)
- [ ] Submit a PySpark job to the K8s Spark Cluster
