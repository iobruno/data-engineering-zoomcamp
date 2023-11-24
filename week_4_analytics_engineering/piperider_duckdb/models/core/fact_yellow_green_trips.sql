{{ config(materialize='table') }}


WITH green_tripdata AS (
    SELECT
        g.*,
        'green' AS service_type,
        -- deduplication logic for green: 1/2
        ROW_NUMBER() OVER( PARTITION BY vendor_id, pickup_datetime ) AS row_num
    FROM
        {{ ref('stg_green_tripdata') }} g
    WHERE
        vendor_id IS NOT NULL
),

yellow_tripdata AS (
    SELECT
        y.*,
        'yellow' AS service_type,
        -- deduplication logic for yellow: 1/2
        ROW_NUMBER() OVER ( PARTITION BY vendor_id, pickup_datetime ) AS row_num
    FROM
        {{ ref('stg_yellow_tripdata') }} y
    WHERE
        vendor_id IS NOT NULL
),

all_tripdata AS (
    -- deduplication logic for green: 2/2
    SELECT * FROM green_tripdata
    WHERE row_num = 1

    UNION ALL

    -- deduplication logic for yellow: 2/2
    SELECT * FROM yellow_tripdata
    WHERE row_num = 1
),

lookup_zones AS (
    SELECT * FROM {{ ref('dim_zone_lookup' )}}
    WHERE borough != 'Unknown'
)

SELECT
    t.trip_id,
    t.vendor_id,
    t.service_type,
    t.ratecode_id,
    t.pickup_location_id,
    pickup.borough               AS pickup_borough,
    pickup.zone                  AS pickup_zone,
    t.dropoff_location_id,
    dropoff.borough              AS dropoff_borough,
    dropoff.zone                 AS dropoff_zone,
    t.pickup_datetime,
    t.dropoff_datetime,
    t.store_and_fwd_flag,
    t.passenger_count,
    t.trip_distance,
    t.trip_type,
    t.fare_amount,
    t.extra,
    t.mta_tax,
    t.tip_amount,
    t.tolls_amount,
    t.ehail_fee,
    t.improvement_surcharge,
    t.total_amount,
    t.payment_type,
    t.congestion_surcharge

FROM all_tripdata t
INNER JOIN lookup_zones pickup  ON t.pickup_location_id  = pickup.location_id
INNER JOIN lookup_zones dropoff ON t.dropoff_location_id = dropoff.location_id
