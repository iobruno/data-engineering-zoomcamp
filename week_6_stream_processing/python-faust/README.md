# Python Stream Processing with Kafka

This subproject builds on top of `faust`, a high-level stream processing framework built on top of `confluent-kafka-python` to develop apps Stream Processing apps

## Tech Stack
- Python 3.9 / 3.10
- Confluent Kafka
- [Faust Streaming](https://github.com/faust-streaming/faust)
- Jupyter Notebook
- [Poetry](https://python-poetry.org/docs/)

## Up and Running

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.10 with conda:
```shell
conda create -n faust-streaming python=3.10 -y
conda activate faust-streaming
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
poetry install --no-root
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

## TODO:
- [X] Set up an environment for Python, Kafka
- [ ] Explore serialization with JSON
- [ ] Explore serialization with Avro
- [ ] Explore KafkaStreams as built-in library in the App
- [ ] Set up a Schema Registry
