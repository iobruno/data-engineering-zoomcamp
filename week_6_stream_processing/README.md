# ksqlDB for Stream Processing

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

CLI v7.3.2, Server v7.3.2 located at http://ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
```

## Tech Stack
- Confluent Kafka (with Zookeeper)
- Confluent Schema Registry
- Confluent REST Proxy
- [ksqlDB](https://ksqldb.io/)
- [Confluent Control Center](https://docs.confluent.io/platform/current/control-center/overview.html)
- [Conduktor Platform](https://www.conduktor.io/explorer/)
- [kpow](https://docs.kpow.io/ce/)
- Docker, docker-compose


## Up and Running

### Architecture Notice
- Take notice that all docker images pulled use `linux/arm64` platform architecture, as I'm using Apple Sillicon (M1).
- Switch that to `linux/amd64` from `linux/arm64`, if you're using an Intel/AMD CPU (x86_64 / amd64) architecture


### Developer Setup

**Note for Windows Users**:

You'll have to ensure that `userid:1000`, `groupid:1000` have read/write permissions for the bind mounts setup on docker-compose.yml
```shell
mkdir -p confluent-data/zk-data
mkdir -p confluent-data/zk-txn-logs
mkdir -p confluent-data/kafka_0
mkdir -p confluent-data/kafka_1
mkdir -p confluent-data/kafka_2
```

```shell
chown -R 1000:1000 confluent-data/
```


**1.** Fire up the Confluent Platform and the UIs with:
```
docker-compose up -d
```

**2.** Start up with the ksqlDB CLI
```
docker exec -it cp-ksqldb-cli ksql http://ksqldb-server:8088
```

You should be getting into this console:
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

CLI v7.3.2, Server v7.3.2 located at http://ksqldb-server:8088
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
```

**3.** Pick one of the following 3x tools as a Web UI for Kafka Administration

**NOTE:** Be aware that `Confluent Control Center` is only available for a 30-day trial period.

**3.1.** `Confluent Control Center` Web UI:
```shell
open http://localhost:9021
```

**3.2.** `Conduktor Platform` Web UI:
```shell
open http://localhost:8080
```

Credentials:
- `username:` admin@conduktor.io
- `password:` admin


**3.3.** `kpow` Web UI:

```shell
open http://localhost:3000/
```



## TODO:
- [x] Set up a Kafka Cluster with ZooKeeper
- [x] Set up Confluent Schema Registry
- [x] Set up Confluent Rest Proxy
- [x] Set up ksqlDB Server and CLI
- [x] Set up `kpow` Web UI
- [x] Set up `Conduktor Platform` Web UI
- [x] Set up a `UI for Kafka` Web UI
- [ ] Switch Kafka to use KRaft instead
