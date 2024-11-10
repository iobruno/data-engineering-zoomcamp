# Stream processing with Kafka & ksqlDB

![Kafka](https://img.shields.io/badge/Confluent_Kafka-7.7-141414?style=flat&logo=apachekafka&logoColor=white&labelColor=141414)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This submodule focuses on various approaches for stream processing, such as:

- [Kotlin](kotlin/): Producing and Consuming messages from/to Kafka with Kotlin/Java
- [kSQLDB](ksqldb/): Stream Processing with kSQLDB (Kafka Streams)
- [RisingWave](risingwave/): Stream Processing with RisingWave

Hop into their respective folders for details on how to spin them up.

**Note**: They all use the same [docker-compose.yml](docker-compose.yml) to bootstrap the kafka cluster. So read the **Up and Running** instructions down below on how to set it up.


## Tech Stack
- Confluent Kafka
- Confluent Schema Registry
- Confluent REST Proxy
- [ksqlDB](https://ksqldb.io/)
- [Conduktor Platform](https://v2.conduktor.io/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Developer Setup

**1.** Spin up Kafka Broker with one of the following options:

1.1. Kafka Cluster (Single-broker) with KRaft:
```shell
docker compose up -d
```

1.2. Kafka Cluster (Multi-broker) with KRaft:
```shell
docker compose -f compose.kraft-multi-broker.yaml up -d
```

1.3. Kafka Cluster (Multi-broker) with Zookeeper:
```shell
docker compose -f compose.zookeeper-multi-broker.yaml up -d
```

1.4. Redpanda:
```shell
docker compose -f compose.redpanda.yaml up -d
```

**2.** Access Conduktor Web UI for Kafka
```shell
open http://localhost:8080
```

## TODO:
- [x] Single-broker Kafka Cluster (with KRaft)
- [x] Multi-broker Kafka Cluster (with KRaft)
- [x] Multi-broker Kafka Cluster (with Zookeeper)
- [x] Confluent Schema Registry
- [x] Confluent Rest Proxy
- [x] ksqlDB Server and CLI
- [x] Kafka Admin UI: `Conduktor Console`
- [ ] Deploy Kafka Cluster (with Zookeeper or KRaft) on K8s using Helm Charts
