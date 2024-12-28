# Batch processing with Spark

![Python](https://img.shields.io/badge/Python-3.12_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Kotlin](https://img.shields.io/badge/Kotlin-2.x-262A38?style=flat-square&logo=kotlin&logoColor=603DC0&labelColor=262A38)
![Scala](https://img.shields.io/badge/Scala-2.12-262A38?style=flat-square&logo=scala&logoColor=E03E3C&labelColor=262A38)
![Spark](https://img.shields.io/badge/Apache_Spark-3.5-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

```
Spark context Web UI available at http://192.168.15.91:4040
Spark context available as 'sc' (master = local[*], app id = local-1735415642729).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.3
      /_/
         
Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.13)
Type in expressions to have them evaluated.
Type :help for more information.

scala>
```

## Tech Stack
- [Kotlin Spark API](https://github.com/Kotlin/kotlin-spark-api)
- [Scala+Spark](https://spark.apache.org/docs/latest/)
- [PySpark](https://spark.apache.org/docs/latest/api/python/user_guide)
- [Docker](https://docs.docker.com/get-docker/)

## Up and Running

**1.** Spin up the Spark Cluster
```shell
docker compose up -d
```

**2.** Refer to the specific implementations for docs on how to run the pipeline:
- [Kotlin](./kotlin/)
- [Scala](./scala/)
- [PySpark](./pyspark/)

## TODO:
- [ ] Batch Processing with PySpark
- [ ] Batch Processing with Spark and Kotlin-Spark-API
- [ ] Batch Processing with Scala+Spark
