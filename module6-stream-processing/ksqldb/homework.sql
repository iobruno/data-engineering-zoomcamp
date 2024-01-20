-- Drop Tables and Streams to reset ksqlDB
DROP TABLE IF EXISTS overall_pickup_agg   DELETE TOPIC;
DROP TABLE IF EXISTS overall_pickup_stats DELETE TOPIC;

DROP TABLE IF EXISTS green_tripdata_stats DELETE TOPIC;
DROP TABLE IF EXISTS fhv_tripdata_stats   DELETE TOPIC;

DROP STREAM IF EXISTS green_tripdata_stream;
DROP STREAM IF EXISTS fhv_tripdata_stream;


-- Config Offset for 'earliest'
SET 'auto.offset.reset' = 'earliest';


-- KStream and KTable for Green Tripdata
CREATE SOURCE STREAM green_tripdata_stream (
    vendor_id INT,
    pickup_location_id INT
) WITH (
    kafka_topic = 'green_tripdata',
    key_format = 'kafka',
    value_format = 'json'
);

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


-- KStream and KTable for FHV Tripdata
CREATE SOURCE STREAM fhv_tripdata_stream (
    dispatching_base_number VARCHAR,
    pickup_location_id INT
) WITH (
    kafka_topic  = 'fhv_tripdata',
    key_format   = 'kafka',
    value_format = 'json'
);

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


-- KTable for Statistics
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
    EMIT CHANGES
;
