# Kafka for Stream Processing with Kotlin

This subproject builds on top of `kafka` and `kafka-streams` to develop Stream Processing Playground

## Tech Stack
- Kotlin (JDK 11 / 17)
- Confluent Kafka
- Kafka Streams
- Gradle

## Up and Running

### Developer Setup

**1.** Install `JDK` 11 or 17. You can do so easily with [SDKMAN!](https://sdkman.io/):

```shell
sdk i java 17.0.6-librca
```

**2.** (Optional) Install `Gradle` version `8.x` with:

```shell
sdk i gradle 8.0.2
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**4.** Build and generate the application artifact:
```shell
gradle clean shadowJar
```

**5.** Run the application with and check the subcommands:
```shell
java -jar java -jar build/libs/kafka-stream-processing-1.0.jar
```

## TODO:
- [x] Set up an environment for Kotlin, Kafka Client and KafkaStreams
- [x] Set up a Schema Registry
- [x] Build a Cli Application for Producer and Consumer
- [x] Explore serialization with JSON
- [ ] Explore serialization with Avro
- [ ] Explore KafkaStreams as built-in library in the App
