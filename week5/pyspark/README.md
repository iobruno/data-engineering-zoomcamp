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

**1.** Install JDK 11 or 17. You can do so easily with [SDKMAN!](https://sdkman.io/):

```
sdk i java 17.0.6-librca
```
or 
```
sdk i java 11.0.18-librca
```

And then, install the project dependencies with:
```
poetry install --no-root
```


## TODO:
- [X] Set up a Jupyter Playground for PySpark
- [x] Explore the SparkSQL API
- [ ] Set up a Standalone Cluster for Spark
- [ ] Submit a PySpark job to the Cluster
