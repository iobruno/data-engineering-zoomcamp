# ksqlDB Stream Processing with KStreams and KTables

This contains the SQL statements to build the KStreams and KTables for ksqlDB to allow an overview of Green and FHV Trips distribution

![ksqldb-streams](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week6_ksqldb_streams.png)


## Tech Stack
- Confluent Kafka
- ksqlDB Server
- ksqlDB CLI
- Docker / Docker-compose

## Up & Running

**0.** Make sure `ksqlDB-server` and `ksql-cli` are up, with [INSTRUCTIONS](https://github.com/iobruno/data-engineering-zoomcamp/tree/master/week_6_stream_processing):
```
docker-compose up -d
```

**1.** Log into ksql-cli Console with:
```
docker exec -it cp-ksqldb-cli ksql http://ksqldb-server:8088
```

**2.** Config ksql to default fetching offsets from 'earliest'
```sql
SET 'auto.offset.reset' = 'earliest';
```

**3.** Create the KStreams for `green_tripdata` and `fhv_tripdata`:
```sql
CREATE SOURCE STREAM green_tripdata_stream (
    vendor_id INT,
    pickup_location_id INT
) WITH (
    kafka_topic = 'green_tripdata',
    key_format = 'kafka',
    value_format = 'json'
);

CREATE SOURCE STREAM fhv_tripdata_stream (
    dispatching_base_number VARCHAR,
    pickup_location_id INT
) WITH (
    kafka_topic  = 'fhv_tripdata',
    key_format   = 'kafka',
    value_format = 'json'
);
```

**4.** Create KTables to count the number of trips per location
```sql
CREATE OR REPLACE TABLE green_tripdata_stats WITH (
    kafka_topic='green_tripdata_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) AS
    SELECT
        pickup_location_id,
        COUNT(*) as num_trips
    FROM green_tripdata_stream
    GROUP BY pickup_location_id
    EMIT CHANGES
;

CREATE OR REPLACE TABLE fhv_tripdata_stats WITH (
    kafka_topic='fhv_pickup_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) AS
    SELECT
        pickup_location_id,
        COUNT(*) as num_trips
    FROM fhv_tripdata_stream
    GROUP BY pickup_location_id
    EMIT CHANGES
;
```

**5.** Create the KTable to joining the `green` and `fhv` tripdata:
```sql
CREATE OR REPLACE TABLE overall_pickup_stats WITH (
    kafka_topic='overall_pickup_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) AS
    SELECT
        ROWKEY as id,
        g.pickup_location_id as green_location_id,
        f.pickup_location_id as fhv_location_id,
        COALESCE(g.num_trips, CAST(0 as BIGINT)) as green_records,
        COALESCE(f.num_trips, CAST(0 as BIGINT)) as fhv_records,
        COALESCE(g.num_trips, CAST(0 as BIGINT)) + COALESCE(f.num_trips, CAST(0 as BIGINT)) as total_records,
        1 as dummy_col -- workaround for overall_pickup_agg
    FROM green_tripdata_stats as g
    FULL OUTER JOIN fhv_tripdata_stats as f ON g.pickup_location_id = f.pickup_location_id
;
```

**6.** Create the KTable to generate the statistics on Trips distribution:
```sql
-- KTable for Statistics on Aggregation
CREATE OR REPLACE TABLE overall_pickup_agg WITH (
    kafka_topic='overall_pickup_agg',
    key_format='kafka',
    value_format='json',
    partitions=2
) AS
    SELECT
        SUM(green_records) as total_green_records,
        SUM(fhv_records)   as total_fhv_records,
        SUM(total_records) as overall_records,
        dummy_col
    FROM overall_pickup_stats
    GROUP BY dummy_col
;
```
**7.** Query the statistics on Trips Distribution with:

```sql
-- Bind to the console to all updates on Query:
ksql> select * from overall_pickup_agg emit changes;

+----------------------+----------------------+----------------------+----------------------+
|DUMMY_COL             |TOTAL_GREEN_RECORDS   |TOTAL_FHV_RECORDS     |OVERALL_RECORDS       |
+----------------------+----------------------+----------------------+----------------------+
|1                     |630918                |21039983              |21670901              |
|1                     |630918                |21058899              |21689817              |
|1                     |630918                |21077704              |21708622              |
|1                     |630918                |21096012              |21726930              |
|1                     |630918                |21115601              |21746519              |
|1                     |630918                |21134044              |21764962              |
|1                     |630918                |21152782              |21783700              |
|1                     |630918                |21170356              |21801274              |
|1                     |630918                |21189974              |21820892              |
|1                     |630918                |21209372              |21840290              |
|1                     |630918                |21226677              |21857595              |
|1                     |630918                |21245814              |21876732              |
|1                     |630918                |21264974              |21895892              |
|1                     |630918                |21284161              |21915079              |
|1                     |630918                |21302856              |21933774              |
|1                     |630918                |21319461              |21950379              |
|1                     |630918                |21323952              |21954870              |
```