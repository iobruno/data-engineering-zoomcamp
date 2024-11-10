# Big Data ecosystem

![Trino](https://img.shields.io/badge/Presto-262A38?style=flat-square&logo=trino&logoColor=E8F5F5&labelColor=262A38)
![Hive](https://img.shields.io/badge/Apache_Hive-FDEE21?style=flat-square&logo=apachehive&logoColor=black&labelColor=FDEE21)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

Big Data playground in Docker, compatible with Apple Sillicon:
- Presto/Trino (Query Engine)
- Hive Metastore
- Hive Server

## Tech Stack
- [Apache Hive](https://hive.apache.org/)
- [Trino](https://trino.io/)
- [Docker](https://docs.docker.com/get-docker/)

## Up and Running

**1.** Spin up the whole stack with docker-compose:
```shell
docker compose up -d
```

**2.** Web UIs can be accessed through:

**2.1.** Presto
```shell
open http://localhost:8080
```

**2.2.** Hive Server
```shell
open http://localhost:10002
```

## TODO:
- [x] Setup Hive Metastore in Docker
- [x] Setup Presto/Trino in Docker
- [ ] Schema evolution w/ Delta/Hive/Presto
