# pandas-SQLAlchemy

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This cli script is set to be able to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones
based on the endpoints in [app.yml](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/pandas_sqlalchemy/app.yml).

- `python sqlalchemy_ingest.py -y` or `--yellow`:
  - fetches the datasets under the key `yellow_trip_data` only
  - persists to Postgres, on table `ntl_yellow_taxi`
  
- `python sqlalchemy_ingest.py -g` or `--green`:
  - fetches the datasets under the key `green_trip_data` only,
  - persists to Postgres, on table `ntl_green_taxi`

- `python sqlalchemy_ingest.py -f` or `--fhv`:
  - fetches the datasets under the key `zone_lookups`
  - persists to Postgres, on table: `ntl_fhv_taxi`

- `python sqlalchemy_ingest.py -z` or `--zones`:
  - fetches the datasets under the key `zone_lookups`
  - persists to Postgres, on table: `ntl_lookup_zones`

You can use any combination of the three above to fetch more than dataset group at a time.

For instance: `python sqlalchemy_ingest.py -gz` fetches the **NYC Green Trip Data** AND **NYC Lookup Zones**


## Tech Stack
- [pandas](https://pandas.pydata.org/docs/user_guide/)
- [Typer](https://typer.tiangolo.com/tutorial/)
- [Rich CLI](https://github.com/Textualize/rich)
- [PDM](https://pdm-project.org/latest/usage/dependency/)
- [Ruff](https://docs.astral.sh/ruff/configuration/)
- [Docker](https://docs.docker.com/get-docker/)


## Up and Running

### Running on Docker

**1.** Fire up the PostgreSQL and pgAdmin:
```shell
 docker-compose up -d
```

Make sure to uncomment the endpoint lines of the Datasets you want to
fetch on [app.yml](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/postgres_ingest/app.yml)

**2.** Build the Docker image for the Ingestion Script:
```shell
docker build -t taxi_ingest .
```

**3.** Run the script:
```shell
docker run --network pg-network -d taxi_ingest
```

### Developer Setup

**1.** Create and activate a virtualenv for Python 3.11 with conda:
```shell
conda create -n pandas-sqlalchemy python=3.11 -y
conda activate pandas-sqlalchemy
```

**2.** Install the dependencies on `pyproject.toml`:
```shell
pdm sync
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:

pre-commit install
```

**4.** Export ENV VARS to connect to DB:

4.1.: To connect to Postgres:
```shell
export DATABASE_DRIVER=postgres \
export DATABASE_HOST=localhost \
export DATABASE_PORT=5432 \
export DATABASE_NAME=nyc_taxi
export DATABASE_USERNAME=postgres \
export DATABASE_PASSWORD=postgres
```

4.2.: To connect to MySQL:
```shell
export DATABASE_DRIVER=mysql \
export DATABASE_HOST=localhost \
export DATABASE_PORT=3306 \
export DATABASE_NAME=nyc_taxi
export DATABASE_USERNAME=mysql \
export DATABASE_PASSWORD=mysql
```

**5.** Run the script with the intended flags or use `--help`:
```shell
python sqlalchemy_ingest.py --help
```


## Containerization and Testing

**1.** Build the Docker Image with:

```shell
docker build -t pandas_sqlalchemy:latest . --no-cache
```

**2.** Start a container with it:

2.1. PosgreSQL:
```shell
docker run \
  -e DATABASE_DRIVER=postgres \
  -e DATABASE_HOST=postgres \
  -e DATABASE_PORT=5432 \
  -e DATABASE_NAME=nyc_taxi \
  -e DATABASE_USERNAME=postgres \
  -e DATABASE_PASSWORD=postgres \
  --network sqlalchemy \
  --name sqlalchemy_postgres \
  pandas_sqlalchemy
```

2.2. For MySQL:
```shell
docker run \
  -e DATABASE_DRIVER=mysql \
  -e DATABASE_HOST=mysql \
  -e DATABASE_PORT=3306 \
  -e DATABASE_NAME=nyc_taxi \
  -e DATABASE_USERNAME=mysql \
  -e DATABASE_PASSWORD=mysql \
  --network sqlalchemy \
  --name sqlalchemy_mysql \
  pandas_sqlalchemy
```


## TODO:
- [x] PEP-517: Packaging and dependency management with PDM
- [x] Code format/lint with Ruff
- [x] Build a CLI app with `Typer`
- [x] Progress Bars to keep track of the execution with `rich`
- [x] Run/Deploy the project on Docker
- [ ] Enable downloading of multiple datasets in parallel