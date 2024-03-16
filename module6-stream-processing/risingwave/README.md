# Stream Processing in SQL with RisingWave

![Python](https://img.shields.io/badge/Python-3.10_|_3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![Kafka](https://img.shields.io/badge/ConfluentKafka-7.6.x-141414?style=flat&logo=apachekafka&logoColor=white&labelColor=141414)
![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)
![MinIO](https://img.shields.io/badge/MinIO-000110?style=flat&logo=minio&logoColor=C72C49&labelColor=000110)
![etcd](https://img.shields.io/badge/etcd-1E6897?style=flat&logo=etcd&logoColor=FFFFFF&labelColor=275C80)
![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)

![project](../../assets/rw-workshop-project.png)


## Tech Stack
- RisingWave (Stream Processing)
- Kafka (Data Source)
- Clickhouse (Sink)
- MinIO (Storage)
- Etcd (Metadata Storage)

## Up & Running 

```shell
docker compose -f docker-compose.kafka.yml up -d
docker compose up -d 
```

#### Initialize Kafka and Rising Wave with some data
The `seed.py` file contains the logic to process the data and populate RisingWave.

Here we:
1. Process the `taxi_zone` data and insert it into RisingWave. This is just ingested with DML over `psycog`, since it's a small dataset.
2. Process the `trip_data` and insert it into RisingWave. This is ingested via Kafka.

In order to simulate real-time data, we will replace the `timestamp` fields in the `trip_data` with `timestamp`s close to the current time.

Let's start ingestion into RisingWave by running it:
```shell
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
python seed.py --use-streaming
```

Now we can let that run in the background.

Let's open another terminal to create the trip_data table:
```shell
psql -f sql/risingwave/table/yellow_taxi_trips.sql
```

You may look at their definitions by running:
```shell
psql -c 'show tables;'
```


#### Validating the ingested data

First, we verify `taxi_zone`, since this is static data:
```sql
select * from taxi_zones;
```

We will also query for recent data, to ensure we are getting real-time data.

```sql
select  
    pulocationid, 
    dolocationid, 
    tpep_pickup_datetime, 
    tpep_dropoff_datetime
from
    yellow_taxi_trips ytt 
where 
    tpep_dropoff_datetime > now() - interval '1 minute';
```


#### Materialized View: 'Latest Trip Data':
We can join this with `taxi_zone` to get the names of the zones and create a materialized view out of it

```sql
create materialized view latest_1min_trip_data as
select
    puz.zone as pickup_zone,
    doz.zone as dropoff_zone,
    tpep_pickup_datetime,
    tpep_dropoff_datetime
from
    yellow_taxi_trips ytt
inner join
    taxi_zones puz on ytt.PULocationID = puz.location_id
inner join
    taxi_zones doz on ytt.DOLocationID = doz.location_id
where
    tpep_dropoff_datetime > now() - interval '1 minute';
```

We can now query the MV to see the latest data:
```sql
select * 
from latest_1min_trip_data 
order by tpep_dropoff_datetime desc;
```


### Materialized View 1: Total Airport Pickups

The first materialized view we create will be to count the total number of pickups at the airports.

This is rather simple, we just need to filter the `PULocationID` to the airport IDs.
 
Recall `taxi_zone` contains metadata around the taxi zones, so we can use that to figure out the airport zones.
```sql
describe taxi_zones;
```

Let's first get the zone names by looking at the `taxi_zone` table:
```sql
select * 
from taxi_zones tz
where zone like '%Airport';
```

Then we can simply join on their location ids to get all the trips:
```sql
select
    *
from
    yellow_taxi_trips ytt
inner join 
    taxi_zones tz on ytt.PULocationID = tz.location_id
where
    tz.zone like '%Airport';
```

And finally apply the `count(*)` aggregation for each airport.  
We can now create a Materialized View to constantly query the latest data:

```sql
create materialized view total_airport_pickups as
select
    tz.zone,
    count(*) AS num_trips
from
    yellow_taxi_trips ytt
inner join 
    taxi_zones tz on ytt.PULocationID = tz.location_id
where 
    tz.zone like '%Airport'
group by 
    tz.zone;
```

We can now query the MV to see the latest data:
```sql
select * 
from total_airport_pickups;
```

#### Visualize the Data
Go to your local [RisingWave Dashboard](http://localhost:5691) to see the query plan.

Provided a simplified a simpler version here:

![query_plan](../../assets/rw-matview-plan-simple.png)


#### Materialized View 2: Airport pickups from JFK Airport, 1 hour before the latest pickup

We can adapt the previous MV to create a more specific one.
We no longer need the `GROUP BY`, since we are only interested in 1 taxi zone, JFK Airport.

```sql
create materialized view airport_pu as
select
    tpep_pickup_datetime,
    pulocationid
from
    yellow_taxi_trips ytt
inner join
    taxi_zones tz on ytt.PULocationID = tz.location_id
where
    tz.Borough = 'Queens' 
    and tz.Zone = 'JFK Airport';
```

Next, we also want to keep track of the latest pickup
```sql
create materialized view latest_jfk_pickup as
select
    max(tpep_pickup_datetime) as latest_pickup_time
from
    yellow_taxi_trips ytt
inner join
    taxi_zones tz on ytt.PULocationID = tz.location_id
where
    tz.borough = 'Queens' 
    and tz.zone = 'JFK Airport';
```

Finally, let's get the counts of the pickups from JFK Airport, 1 hour before the latest pickup
```sql
create materialized view jfk_pickups_1hr_before as
select
    count(*) AS num_trips
from
    airport_pu air
inner join
    latest_jfk_pickup jfk on air.tpep_pickup_datetime > jfk.latest_pickup_time - interval '1 hour'
inner join 
    taxi_zones tz on air.PULocationID = tz.location_id
where
    tz.borough = 'Queens' 
    and tz.zone = 'JFK Airport';
```

Simplified query plan:
![query_plan](../../assets/rw-matview-plan-dynfilter.png)


#### Materialized View 3: Top 10 busiest zones in the last 1 minute

First we can write a query to get the counts of the pickups from each zone.
```sql
select
    tz.zone as dropoff_zone,
    count(*) as last_1_min_dropoffs
from
    yellow_taxi_trips ytt
inner join 
    taxi_zones tz on ytt.DOLocationID = tz.location_id
group by
    tz.zone
order by 
    last_1_min_dropoffs desc
limit 10;
```

Next, we can create a temporal filter to get the counts of the pickups from each zone in the last 1 minute.

```sql
create materialized view busiest_zones_1_min as
select
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    puz.Zone as pickup_zone,
    doz.Zone as dropoff_zone,
    trip_distance
from
    yellow_taxi_trips ytt
inner join 
    taxi_zones puz on ytt.PULocationID = puz.location_id
inner join 
    taxi_zones doz on ytt.DOLocationID = doz.location_id
order by
    trip_distance desc
limit 
    10;
```

Didn't include the query plan this time, you may look at the dashboard.

#### Materialized View 4: Longest trips

Here, the concept is similar as the previous MV, but we are interested in the top 10 longest trips for the last 5 min.

First we create the query to get the longest trips:
```sql
select
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    puz.Zone as pickup_zone,
    doz.Zone as dropoff_zone,
    trip_distance
from
    yellow_taxi_trips ytt
inner join 
    taxi_zones puz on ytt.PULocationID = puz.location_id
inner join 
    taxi_zones doz on ytt.DOLocationID = doz.location_id
order by
    trip_distance desc
limit 
    10;
```

Then we can create a temporal filter to get the longest trips for the last 5 minutes:
```sql
create materialized view longest_trip_1_min as
select 
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    puz.zone as pickup_zone,
    doz.zone as dropoff_zone,
    trip_distance
from 
    yellow_taxi_trips ytt
inner join
    taxi_zones puz on ytt.PULocationID = puz.location_id
inner join
    taxi_zones doz on ytt.DOLocationID = doz.location_id
where
    ytt.tpep_pickup_datetime > (now() - interval '5' minute)
order by
    trip_distance desc
limit 
    10;
```

Didn't include the query plan this time, you may look at the dashboard.

After this, you may run the visualization dashboard to see the data in real-time.

Start the backend which queries RisingWave:
```shell
python webapp/api.py
```

#### Visualize Data from Materialized View 3 and 4

Start the frontend, in a separate terminal
```shell
### macOS
open webapp/index.html

### Linux
xdg-open webapp/index.html
```

#### Materialized View 5: Average Fare Amount vs Number of rides

How does `avg_fare_amount` change relative to number of pickups per minute?

We use something known as a [tumble window function](https://docs.risingwave.com/docs/current/sql-function-time-window/#tumble-time-window-function), to compute this.

```sql
create materialized view avg_fare_amount as
select
    avg(fare_amount) as avg_fare_amount_per_min,
    count(*) as num_rides_per_min,
    window_start,
    window_end
from
    tumble(yellow_taxi_trips, tpep_pickup_datetime, interval '1' minute)
group by
    window_start, 
    window_end
order by
    num_rides_per_min asc;
```

For each window we compute the average fare amount and the number of rides. That's all for the materialized views!

Now we will see how to sink the data out from RisingWave.


#### How to sink data from RisingWave to Clickhouse

We have done some simple analytics and processing of the data in RisingWave.  
Now we want to sink the data out to Clickhouse, for further analysis.

We will create a Clickhouse table to store the data from the materialized views.

```shell
docker compose -f docker-compose.clickhouse.yml up -d
```

```sql
create table avg_fare_amount(
    avg_fare_amount_per_min numeric,
    num_rides_per_min Int64,
) engine = ReplacingMergeTree
primary key (
    avg_fare_amount_per_min, 
    num_rides_per_min
);
```

We will create a Clickhouse sink to sink the data from the materialized views to the Clickhouse table.

```sql
create sink if not exists avg_fare_amount_sink as 
select
    avg_fare_amount_per_min,
    num_rides_per_min
from
    avg_fare_amount
with (
    connector = 'clickhouse',
    type = 'append-only',
    clickhouse.url = 'http://clickhouse:8123',
    clickhouse.user = 'clickhouse',
    clickhouse.password = 'clickhouse',
    clickhouse.database = 'default',
    clickhouse.table='avg_fare_amount',
    force_append_only = 'true'
);
```

Now we can run queries on the data ingested into clickhouse:
```shell
clickhouse-client-term
```

Run some queries in `Clickhouse`
```sql
select max(avg_fare_amount_per_min) 
from avg_fare_amount;
```
```sql
select min(avg_fare_amount_per_min) 
from avg_fare_amount;
```

## References
- https://tutorials.risingwave.com/docs/category/basics
- https://docs.risingwave.com/docs/current/risingwave-docker-compose/
- https://docs.risingwave.com/docs/current/ingest-from-kafka/
- https://docs.risingwave.com/docs/current/data-ingestion/
- https://docs.risingwave.com/docs/current/sink-to-clickhouse/
- https://docs.risingwave.com/docs/current/data-delivery/
