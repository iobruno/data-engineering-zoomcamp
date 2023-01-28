# Postgres Ingest

Find the answers to [**Homework 1 Part A here**](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/postgres_ingest/HOMEWORK.md)

This cli script is set to be able to fetch the CSV datasets for NYC Yellow Trip Data, Green Trip Data, and Lookup Zones 
based on the endpoints in [app.yml](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/postgres_ingest/app.yml).

- `python pg_ingest.py -g` or `--with-green-data`: 
  - fetches the datasets under the key `green_trip_data` only, 
  - persists to Postgres, on table `green_trip_data`

- `python pg_ingest.py -y` or `--with-yellow-data`:
  - fetches the datasets under the key `yellow_trip_data` only  
  - persists to Postgres, on table `ntl_yellow_taxi`

- `python pg_ingest.py -z` or `--with-lookup-zones`:
  - fetches the datasets under the key `zone_lookups`
  - persists to Postgres, on table: `ntl_lookup_zones` 

You can use any combination of the three above to fetch more than dataset group at a time.  
For instance: `python pg_ingest.py -gz` fetches the **NYC Green Trip Data** AND **NYC Lookup Zones**

Check the details on how to run with Docker or Locally on the `Up and Running` section

![data-eng-zoomcamp-postgres-ingest](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/postgres_ingest/docs/de-zoomcamp-postgres-ingest.gif)

## Tech Stack
- Python 3.9.+
- **Dataframe**: pandas, numpy
- **CLI**: `click`, `rich` 
- **Virtualenv**: Conda
- **Dependency Management**: Poetry
- **Containers**: Docker, docker-compose

## Up and Running

### Running on Docker

- Start by firing up postgres and pgAdmin: 
```bash
 docker-compose up -d
```

- Make sure to uncomment the endpoint lines of the Datasets you want to fetch on [app.yml](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/postgres_ingest/app.yml)
- Build the Docker image for the Ingestion Script:
```bash
docker build -t taxi_ingest .
``` 
- Run the script:
```bash
docker run --network pg-network -it taxi_ingest
```


### Developer Setup

- Create and activate a virtualenv for Python 3.9 with conda
```bash
conda create -n de-zoomcamp python=3.9 -y
conda activate de-zoomcamp
```
- Install the dependencies on `pyproject.toml`:
```bash
poetry install --no-root
```
- Export ENV VARS to connect to DB:
```bash
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=postgres
export DATABASE_HOST=localhost
export DATABASE_PORT=5433
export DATABASE_NAME=ny_taxi
```
- Run the script with the intended flags or use `--help`
```bash
python pg_ingest.py --help
```

## TODO:
- [x] Externalize endpoints to config file
- [x] Build a CLI app with `click`
- [x] Progress Bars to keep track of the execution with `rich`
- [ ] Replace requirement.txt files with Poetry and `pyproject.toml`
