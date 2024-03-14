# Stream Processing in SQL with RisingWave

![project](./assets/project.png)

Before beginning on this section, make sure you have setup your environment according to the [README](./README.md).

Note that in every new terminal you should run the following command to load the environment variables and commands:
```bash
source commands.sh
```

## Setting up RisingWave with Docker Compose

Reference: https://docs.risingwave.com/docs/current/risingwave-docker-compose/

For this workshop, I have slightly modified the `docker-compose.yml` file to include clickhouse as well.

The `docker-compose.yml` file is located in the `docker` directory.

It contains the following key components:
- RisingWave (Stream Processing)
- Clickhouse (Downstream Delivery)
- Redpanda (Upstream Ingestion)
- Grafana (Visualization)
- Prometheus (Metrics)
- MinIO (Storage)
- Etcd (Metadata Storage)

## Ingesting Data into RisingWave using Kafka

Reference:
- https://docs.risingwave.com/docs/current/ingest-from-kafka/
- https://docs.risingwave.com/docs/current/data-ingestion/

The `seed_kafka.py` file contains the logic to process the data and populate RisingWave.

Here we:
1. Process the `taxi_zone` data and insert it into RisingWave. This is just ingested with DML over `psycog`, since it's a small dataset.
2. Process the `trip_data` and insert it into RisingWave. This is ingested via Kafka.

In order to simulate real-time data, we will replace the `timestamp` fields in the `trip_data` with `timestamp`s close to the current time.

Let's start ingestion into RisingWave by running it:
```bash
stream-kafka
```

Now we can let that run in the background.

Let's open another terminal to create the trip_data table:
```bash
source commands.sh
psql -f risingwave-sql/table/trip_data.sql
```

You may look at their definitions by running:
```bash
psql -c 'SHOW TABLES;'
```

## Stream Processing with Materialized Views in RisingWave

### Validating the ingested data

Now we are ready to begin processing the real-time stream being ingested into RisingWave!

The first thing we will do is to check `taxi_zone` and `trip_data`, to make sure
the data has been ingested correctly.

Let's start a `psql` session.
```bash
source commands.sh
psql
```

First, we verify `taxi_zone`, since this is static data:
```sql
SELECT * FROM taxi_zone;
```

We will also query for recent data, to ensure we are getting real-time data.

```sql
SELECT pulocationid, dolocationid, tpep_pickup_datetime, tpep_dropoff_datetime
FROM trip_data WHERE tpep_dropoff_datetime > now() - interval '1 minute';
```

We can join this with `taxi_zone` to get the names of the zones.

```sql
SELECT taxi_zone.Zone as pickup_zone, taxi_zone_1.Zone as dropoff_zone, tpep_pickup_datetime, tpep_dropoff_datetime
 FROM trip_data
 JOIN taxi_zone ON trip_data.PULocationID = taxi_zone.location_id
 JOIN taxi_zone as taxi_zone_1 ON trip_data.DOLocationID = taxi_zone_1.location_id
 WHERE tpep_dropoff_datetime > now() - interval '1 minute';
```

And finally make it into an MV so we can constantly query the latest realtime data:
```sql
CREATE MATERIALIZED VIEW latest_1min_trip_data AS
 SELECT taxi_zone.Zone as pickup_zone, taxi_zone_1.Zone as dropoff_zone, tpep_pickup_datetime, tpep_dropoff_datetime
 FROM trip_data
 JOIN taxi_zone ON trip_data.PULocationID = taxi_zone.location_id
 JOIN taxi_zone as taxi_zone_1 ON trip_data.DOLocationID = taxi_zone_1.location_id
 WHERE tpep_dropoff_datetime > now() - interval '1 minute';
```

We can now query the MV to see the latest data:
```sql
SELECT * FROM latest_1min_trip_data order by tpep_dropoff_datetime DESC;
```

Now we can start processing the data with Materialized Views, to provide analysis of the data stream!

### Materialized View 1: Total Airport Pickups

The first materialized view we create will be to count the total number of pickups at the airports.

This is rather simple, we just need to filter the `PULocationID` to the airport IDs.
 
Recall `taxi_zone` contains metadata around the taxi zones, so we can use that to figure out the airport zones.
```sql
describe taxi_zone;
```

Let's first get the zone names by looking at the `taxi_zone` table:
```sql
SELECT * FROM taxi_zone WHERE Zone LIKE '%Airport';
```

Then we can simply join on their location ids to get all the trips:
```sql
    SELECT
        *
    FROM
        trip_data
            JOIN taxi_zone
                 ON trip_data.PULocationID = taxi_zone.location_id
    WHERE taxi_zone.Zone LIKE '%Airport';
```

And finally apply the `count(*)` aggregation for each airport.

```sql
    SELECT
        count(*) AS cnt,
        taxi_zone.Zone
    FROM
        trip_data
            JOIN taxi_zone
                 ON trip_data.PULocationID = taxi_zone.location_id
    WHERE taxi_zone.Zone LIKE '%Airport'
    GROUP BY taxi_zone.Zone;
```

We can now create a Materialized View to constantly query the latest data:
```sql
CREATE MATERIALIZED VIEW total_airport_pickups AS
    SELECT
        count(*) AS cnt,
        taxi_zone.Zone
    FROM
        trip_data
            JOIN taxi_zone
                ON trip_data.PULocationID = taxi_zone.location_id
    WHERE taxi_zone.Zone LIKE '%Airport'
    GROUP BY taxi_zone.Zone;
```

We can now query the MV to see the latest data:
```sql
SELECT * FROM total_airport_pickups;
```

So what actually happens for the MV?

We can examine the query plan to see what's happening:
```sql
EXPLAIN CREATE MATERIALIZED VIEW total_airport_pickups AS
    SELECT
        count(*) AS cnt,
        taxi_zone.Zone
    FROM
        trip_data
            JOIN taxi_zone
                 ON trip_data.PULocationID = taxi_zone.location_id
    WHERE taxi_zone.Zone LIKE '%Airport'
    GROUP BY taxi_zone.Zone;
```

```
                                                    QUERY PLAN                                                    
------------------------------------------------------------------------------------------------------------------
 StreamMaterialize { columns: [cnt, zone], stream_key: [zone], pk_columns: [zone], pk_conflict: NoCheck }
 └─StreamProject { exprs: [count, taxi_zone.zone] }
   └─StreamHashAgg { group_key: [taxi_zone.zone], aggs: [count] }
                                                  ^-- apply the count aggregation
     └─StreamExchange { dist: HashShard(taxi_zone.zone) }
       └─StreamHashJoin { type: Inner, predicate: trip_data.pulocationid = $expr1 }
                                                  ^-- join them with a predicate
         ├─StreamExchange { dist: HashShard(trip_data.pulocationid) }
         │ └─StreamTableScan { table: trip_data, columns: [pulocationid, _row_id] }
                                      ^-- scan from trip_data
         └─StreamExchange { dist: HashShard($expr1) }
           └─StreamProject { exprs: [taxi_zone.zone, taxi_zone.location_id::Int64 as $expr1, taxi_zone._row_id] }
             └─StreamFilter { predicate: Like(taxi_zone.zone, '%Airport':Varchar) }
               └─StreamTableScan { table: taxi_zone, columns: [location_id, zone, _row_id] }
                                           ^-- Scan from taxi_zone
```

Go to your local [RisingWave Dashboard](http://localhost:5691) to see the query plan.

Provided a simplified a simpler version here:

![query_plan](./assets/mv1_plan.png)

```sql
CREATE MATERIALIZED VIEW total_airport_pickups AS
    SELECT
        count(*) AS cnt,
        taxi_zone.Zone
    FROM
        trip_data
            JOIN taxi_zone
                 ON trip_data.PULocationID = taxi_zone.location_id
    WHERE taxi_zone.Zone LIKE '%Airport'
    GROUP BY taxi_zone.Zone;
```

### Materialized View 2: Airport pickups from JFK Airport, 1 hour before the latest pickup

We can adapt the previous MV to create a more specific one.
We no longer need the `GROUP BY`, since we are only interested in 1 taxi zone, JFK Airport.

```sql
CREATE MATERIALIZED VIEW airport_pu as
SELECT
    tpep_pickup_datetime,
    pulocationid
FROM
    trip_data
        JOIN taxi_zone
            ON trip_data.PULocationID = taxi_zone.location_id
WHERE
        taxi_zone.Borough = 'Queens'
  AND taxi_zone.Zone = 'JFK Airport';
```

Next, we also want to keep track of the latest pickup
```sql
CREATE MATERIALIZED VIEW latest_jfk_pickup AS
    SELECT
        max(tpep_pickup_datetime) AS latest_pickup_time
    FROM
        trip_data
            JOIN taxi_zone
                ON trip_data.PULocationID = taxi_zone.location_id
    WHERE
        taxi_zone.Borough = 'Queens'
      AND taxi_zone.Zone = 'JFK Airport';
```

Finally, let's get the counts of the pickups from JFK Airport, 1 hour before the latest pickup
```sql
CREATE MATERIALIZED VIEW jfk_pickups_1hr_before AS
    SELECT
        count(*) AS cnt
    FROM
        airport_pu
            JOIN latest_jfk_pickup
                ON airport_pu.tpep_pickup_datetime > latest_jfk_pickup.latest_pickup_time - interval '1 hour'
            JOIN taxi_zone
                ON airport_pu.PULocationID = taxi_zone.location_id
    WHERE
        taxi_zone.Borough = 'Queens'
      AND taxi_zone.Zone = 'JFK Airport';
```

Simplified query plan:

![query_plan](./assets/mv2_plan.png)

### Materialized View 3: Top 10 busiest zones in the last 1 minute

First we can write a query to get the counts of the pickups from each zone.

```sql
SELECT
    taxi_zone.Zone AS dropoff_zone,
    count(*) AS last_1_min_dropoff_cnt
FROM
    trip_data
        JOIN taxi_zone
            ON trip_data.DOLocationID = taxi_zone.location_id
GROUP BY
    taxi_zone.Zone
ORDER BY last_1_min_dropoff_cnt DESC
    LIMIT 10;
```

Next, we can create a temporal filter to get the counts of the pickups from each zone in the last 1 minute.

That has the form:
```sql
WHERE
    'timestamp-column' > (NOW() - INTERVAL '1' MINUTE)
```

```sql
CREATE MATERIALIZED VIEW busiest_zones_1_min AS SELECT
    taxi_zone.Zone AS dropoff_zone,
    count(*) AS last_1_min_dropoff_cnt
FROM
    trip_data
        JOIN taxi_zone
            ON trip_data.DOLocationID = taxi_zone.location_id
WHERE
    trip_data.tpep_dropoff_datetime > (NOW() - INTERVAL '1' MINUTE)
GROUP BY
    taxi_zone.Zone
ORDER BY last_1_min_dropoff_cnt DESC
    LIMIT 10;
```

Didn't include the query plan this time, you may look at the dashboard.

### Materialized View 4: Longest trips

Here, the concept is similar as the previous MV, but we are interested in the top 10 longest trips for the last 5 min.

First we create the query to get the longest trips:
```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    taxi_zone_pu.Zone as pickup_zone,
    taxi_zone_do.Zone as dropoff_zone,
    trip_distance
FROM
    trip_data
        JOIN taxi_zone as taxi_zone_pu
             ON trip_data.PULocationID = taxi_zone_pu.location_id
        JOIN taxi_zone as taxi_zone_do
             ON trip_data.DOLocationID = taxi_zone_do.location_id
ORDER BY
    trip_distance DESC
    LIMIT 10;
```

Then we can create a temporal filter to get the longest trips for the last 5 minutes:
```sql
CREATE MATERIALIZED VIEW longest_trip_1_min AS SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        taxi_zone_pu.Zone as pickup_zone,
        taxi_zone_do.Zone as dropoff_zone,
        trip_distance
    FROM
        trip_data
    JOIN taxi_zone as taxi_zone_pu
        ON trip_data.PULocationID = taxi_zone_pu.location_id
    JOIN taxi_zone as taxi_zone_do
        ON trip_data.DOLocationID = taxi_zone_do.location_id
    WHERE
        trip_data.tpep_pickup_datetime > (NOW() - INTERVAL '5' MINUTE)
    ORDER BY
        trip_distance DESC
    LIMIT 10;
```

Didn't include the query plan this time, you may look at the dashboard.

After this, you may run the visualization dashboard to see the data in real-time.

Start the backend which queries RisingWave:
```bash
./server.py
```

### Visualize Data from Materialized View 3 and 4

Start the frontend, in a separate terminal, if you're on OSX:
```bash
open index.html
```

Start the frontend, in a separate terminal, if you're on linux:
```bash
xdg-open index.html
```

### Materialized View 5: Average Fare Amount vs Number of rides

How does `avg_fare_amt` change relative to number of pickups per minute?

We use something known as a [tumble window function](https://docs.risingwave.com/docs/current/sql-function-time-window/#tumble-time-window-function), to compute this.

```sql
CREATE MATERIALIZED VIEW avg_fare_amt AS
SELECT
    avg(fare_amount) AS avg_fare_amount_per_min,
    count(*) AS num_rides_per_min,
    window_start,
    window_end
FROM
    TUMBLE(trip_data, tpep_pickup_datetime, INTERVAL '1' MINUTE)
GROUP BY
    window_start, window_end
ORDER BY
    num_rides_per_min ASC;
```

For each window we compute the average fare amount and the number of rides.

That's all for the materialized views!

Now we will see how to sink the data out from RisingWave.

## How to sink data from RisingWave to Clickhouse

Reference:
- https://docs.risingwave.com/docs/current/data-delivery/
- https://docs.risingwave.com/docs/current/sink-to-clickhouse/

We have done some simple analytics and processing of the data in RisingWave.

Now we want to sink the data out to Clickhouse, for further analysis.

We will create a Clickhouse table to store the data from the materialized views.

```sql
CREATE TABLE avg_fare_amt(
    avg_fare_amount_per_min numeric,
    num_rides_per_min Int64,
) ENGINE = ReplacingMergeTree
PRIMARY KEY (avg_fare_amount_per_min, num_rides_per_min);
```

We will create a Clickhouse sink to sink the data from the materialized views to the Clickhouse table.

```sql
CREATE SINK IF NOT EXISTS avg_fare_amt_sink AS SELECT avg_fare_amount_per_min, num_rides_per_min FROM avg_fare_amt
WITH (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = '',
    clickhouse.password = '',
    clickhouse.database = 'default',
    clickhouse.table='avg_fare_amt',
    force_append_only = 'true'
);
```

Now we can run queries on the data ingested into clickhouse:
```bash
clickhouse-client-term
```

Run some queries in `Clickhouse`
```sql
select max(avg_fare_amount_per_min) from avg_fare_amt;
select min(avg_fare_amount_per_min) from avg_fare_amt;
```

## Summary

In this workshop you have learnt:
- How to ingest data into RisingWave using Kafka
- How to process the data using Materialized Views
  - Using Aggregations
  - Using Temporal Filters
  - Using Window Functions (Tumble)
  - Using Joins
  - Layering MVs to build a stream pipeline
- How to sink the data out from RisingWave to Clickhouse

## What's next?

https://tutorials.risingwave.com/docs/category/basics

## Homework

To further understand the concepts, please try the [Homework](./homework.md).