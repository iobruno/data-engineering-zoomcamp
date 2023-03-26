DROP TABLE overall_pickup_stats DELETE TOPIC;
DROP TABLE overall_pickup_agg DELETE TOPIC;
DROP TABLE green_pickup_stats DELETE TOPIC;
DROP TABLE fhv_pickup_stats DELETE TOPIC;
DROP STREAM green_pickup_data;
DROP STREAM fhv_pickup_data;


CREATE SOURCE STREAM green_pickup_data (
    vendor_id VARCHAR,
    pickup_location_id INT
) WITH (
    kafka_topic = 'green_tripdata', 
    value_format = 'json'
);

CREATE SOURCE STREAM fhv_pickup_data (
    dispatching_base_number VARCHAR,
    pickup_location_id INT
) WITH (
    kafka_topic = 'fhv_tripdata',
    value_format = 'json'
);

CREATE OR REPLACE TABLE green_pickup_stats WITH (
    kafka_topic='green_pickup_stats', 
    value_format='json', 
    partitions=4
) AS 
    SELECT
        g.pickup_location_id,
        COUNT(*) as num_records
    FROM green_pickup_data g
    GROUP BY g.pickup_location_id
    EMIT CHANGES
;

CREATE OR REPLACE TABLE fhv_pickup_stats WITH (
    kafka_topic='fhv_pickup_stats', 
    value_format='json', 
    partitions=4
) AS 
    SELECT 
        f.pickup_location_id,
        COUNT(*) as num_records
    FROM fhv_pickup_data f
    GROUP BY f.pickup_location_id
    EMIT CHANGES
;

CREATE OR REPLACE TABLE overall_pickup_agg WITH (
    kafka_topic='overall_pickup_agg',
    value_format='json',
    partitions=4
) AS 
    SELECT 
        ROWKEY as id,
        g.pickup_location_id as green_pickup_location_id,
        f.pickup_location_id as fhv_pickup_location_id,
        COALESCE(g.num_records, CAST(0 as BIGINT)) as green_records,
        COALESCE(f.num_records, CAST(0 as BIGINT)) as fhv_records,
        COALESCE(g.num_records, CAST(0 as BIGINT)) + COALESCE(f.num_records, CAST(0 as BIGINT)) as total_records 
    FROM green_pickup_stats as g
    FULL OUTER JOIN fhv_pickup_stats as f ON g.pickup_location_id = f.pickup_location_id
    EMIT CHANGES
;

CREATE OR REPLACE TABLE overall_pickup_stats WITH (
    kafka_topic='overall_pickup_stats',
    value_format='json',
    partitions=4
) AS 
    SELECT 
        id,
        green_pickup_location_id,
        fhv_pickup_location_id,
        green_records,
        fhv_records,
        total_records,
        CAST(green_records/total_records AS DECIMAL(4,4)) as green_dist,
        CAST(fhv_records/total_records AS DECIMAL(4,4)) as fhv_dist
    FROM overall_pickup_agg
;