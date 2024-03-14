<p align="center">
  <picture>
    <source srcset="https://github.com/risingwavelabs/risingwave/blob/main/.github/RisingWave-logo-dark.svg" width="500px" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/risingwavelabs/risingwave/blob/main/.github/RisingWave-logo-light.svg" width="500px">
  </picture>
</p>


</div>

<p align="center">
  <a
    href="https://docs.risingwave.com/"
    target="_blank"
  ><b>Documentation</b></a>&nbsp;&nbsp;&nbsp;📑&nbsp;&nbsp;&nbsp;
  <a
    href="https://tutorials.risingwave.com/"
    target="_blank"
  ><b>Hands-on Tutorials</b></a>&nbsp;&nbsp;&nbsp;🎯&nbsp;&nbsp;&nbsp;
  <a
    href="https://cloud.risingwave.com/"
    target="_blank"
  ><b>RisingWave Cloud</b></a>&nbsp;&nbsp;&nbsp;🚀&nbsp;&nbsp;&nbsp;
  <a
    href="https://risingwave.com/slack"
    target="_blank"
  >
    <b>Get Instant Help</b>
  </a>
</p>
<div align="center">
  <a
    href="https://risingwave.com/slack"
    target="_blank"
  >
    <img alt="Slack" src="https://badgen.net/badge/Slack/Join%20RisingWave/0abd59?icon=slack" />
  </a>
  <a
    href="https://twitter.com/risingwavelabs"
    target="_blank"
  >
    <img alt="X" src="https://img.shields.io/twitter/follow/risingwavelabs" />
  </a>
  <a
    href="https://www.youtube.com/@risingwave-labs"
    target="_blank"
  >
    <img alt="YouTube" src="https://img.shields.io/youtube/channel/views/UCsHwdyBRxBpmkA5RRd0YNEA" />
  </a>
</div>

## Stream processing in SQL with RisingWave

In this hands-on workshop, we’ll learn how to process real-time streaming data using SQL in RisingWave. The system we’ll use is [RisingWave](https://github.com/risingwavelabs/risingwave), an open-source SQL database for processing and managing streaming data. You may not feel unfamiliar with RisingWave’s user experience, as it’s fully wire compatible with PostgreSQL.

![RisingWave](https://raw.githubusercontent.com/risingwavelabs/risingwave-docs/main/docs/images/new_archi_grey.png)

We will use the NYC Taxi dataset, which contains information
about taxi trips in New York City.

We’ll cover the following topics in this Workshop:

- Why Stream Processing?
- Stateless computation (Filters, Projections)
- Stateful Computation (Aggregations, Joins)
- Data Ingestion and Delivery

RisingWave in 10 Minutes:
https://tutorials.risingwave.com/docs/intro

## Prerequisites

1. Docker and Docker Compose
2. Python 3.7 or later
3. `pip` and `virtualenv` for Python
4. `psql` (I use PostgreSQL-14.9)
5. Clone this repository:
   ```sh
   git clone git@github.com:risingwavelabs/risingwave-data-talks-workshop-2024-03-04.git
   cd risingwave-data-talks-workshop-2024-03-04
   ```
   Or, if you prefer HTTPS:
   ```sh
   git clone https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04.git
   cd risingwave-data-talks-workshop-2024-03-04
   ```

## Note on the dataset

The NYC Taxi dataset is a public dataset that contains information about taxi trips in New York City.
The dataset is available in Parquet format and can be downloaded from the [NYC Taxi & Limousine Commission website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

We will be using the following files from the dataset:
- `yellow_tripdata_2022-01.parquet`
- `taxi_zone.csv`

For your convenience, these have already been downloaded and are available in the `data` directory.

The file `seed_kafka.py` contains the logic to process the data and populate RisingWave.

In this workshop, we will replace the `timestamp` fields in the `trip_data` with `timestamp`s close to the current time.
That's because `yellow_tripdata_2022-01.parquet` contains historical data from 2022,
and we want to simulate processing real-time data.

## Project Structure

```plaintext
$ tree -L 1
.
├── README.md                   # This file
├── clickhouse-sql              # SQL scripts for Clickhouse
├── commands.sh                 # Commands to operate the cluster
├── data                        # Data files (trip_data, taxi_zone)
├── docker                      # Contains docker compose files
├── requirements.txt            # Python dependencies
├── risingwave-sql              # SQL scripts for RisingWave (includes some homework files)
└── seed_kafka.py               # Python script to seed Kafka
```

## Getting Started

Before getting your hands dirty with the project, we will:
1. Run some diagnostics.
2. Start the RisingWave cluster.
3. Setup our python environment.

```bash
# Check version of psql
psql --version
source commands.sh

# Start the RW cluster
start-cluster

# Setup python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`commands.sh` contains several commands to operate the cluster. You may reference it to see what commands are available.

Now you're ready to start on the [workshop](./workshop.md)!