# Stream Processing with Kafka & ksqlDB

```

                  ===========================================
                  =       _              _ ____  ____       =
                  =      | | _____  __ _| |  _ \| __ )      =
                  =      | |/ / __|/ _` | | | | |  _ \      =
                  =      |   <\__ \ (_| | | |_| | |_) |     =
                  =      |_|\_\___/\__, |_|____/|____/      =
                  =                   |_|                   =
                  =        The Database purpose-built       =
                  =        for stream processing apps       =
                  ===========================================

Copyright 2017-2022 Confluent Inc.

CLI v7.4.3, Server v7.4.3 located at http://ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
```

## Tech Stack
- Confluent Kafka
- Confluent Schema Registry
- Confluent REST Proxy
- [ksqlDB](https://ksqldb.io/)
- [Conduktor Platform](https://www.conduktor.io/console/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Start up Kafka Cluster with:

```shell
docker compose up -d
```

**2.** Connect to ksqlDB through the ksqlDB CLI
```
docker exec -it ksqlcli ksql http://ksqldb0:8088
```

You should be getting into this console:
```
ksql>
```

**3.** Access Conduktor Web UI for Kafka

```shell
open http://localhost:8080
```

Credentials:
- `username:` admin@conduktor.io
- `password:` admin


## TODO:
- [x] Set up a Kafka Cluster with ZooKeeper
- [x] Set up Confluent Schema Registry
- [x] Set up Confluent Rest Proxy
- [x] Set up ksqlDB Server and CLI
- [x] Set up `Conduktor Platform` Web UI
- [ ] Deploy Kafka Cluster on K8s with Helm Charts