# Python ingestion with polars and pandas

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Typer](https://img.shields.io/badge/Typer-262A38?style=flat&logo=typer&logoColor=FFFFFF&labelColor=262A38)](https://typer.tiangolo.com/tutorial/)
[![Polars](https://img.shields.io/badge/polars-24292E?style=flat&logo=polars&logoColor=CC792B&labelColor=24292E)](https://docs.pola.rs/)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)](https://pandas.pydata.org/docs/user_guide/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This cli script is set to be able to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones
based on the endpoints in [datasets.yaml](./datasets.yaml).


## Getting Started

**1.** Install dependencies from pyproject.toml and activate the created virtualenv:
```shell
uv sync && source .venv/bin/activate
```

**2.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**3.** Export ENV VARS to connect to DB:
```shell
export DB_HOST=localhost
export DB_NAME=nyc_taxi
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
```

**4.** Run the script with the intended flags or use `--help`:

`ntlcli ingest -y` or `--yellow`:
* fetches the datasets under the key `yellow_trip_data` only
* persists to Postgres, on table `yellow_taxi_data`
  
`ntlcli ingest -g` or `--green`:
* fetches the datasets under the key `green_trip_data` only,
* persists to Postgres, on table `green_taxi_data`

`ntlcli ingest -f` or `--fhv`:
* fetches the datasets under the key `fhv_trip_data`
* persists to Postgres, on table: `fhv_taxi_data`

`ntlcli ingest -z` or `--zones`:
* fetches the datasets under the key `zone_lookups`
* persists to Postgres, on table: `zone_lookup`

Additionally, you can use `--use-polars` for a major speed boost with Polars. 

You can use any combination of options above to fetch more than dataset group at a time. For instance: `ntlcli ingest -gz --use-polars` fetches the **NYC GreenTaxi Trip Data** and **NYC Lookup Zones** while **using Polars** as the Dataframe library.


## Containerization

**1.** Build the Docker Image with:
```shell
docker build -t iobruno/ntlcli:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=5432 \
  -e DB_NAME=nyc_taxi \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  --name ntlcli \
  iobruno/ntlcli
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Code format/lint with Ruff
- [x] Build a CLI app with `Typer`
- [x] Progress Bars to keep track of the execution with `rich`
- [x] Run/Deploy the project on Docker
- [x] Re-Implement the pipeline with Polars
- [x] Define DataFrame schemas for Polars to prevent errors
