## Week 5 Homework

In this homework we'll put what we learned about Spark in practice.
For this homework we will be using the FHVHV 2021-06 data found here. [FHVHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz )


### Question 1:

**Install Spark and PySpark**

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
- [X] 3.3.2
- [ ] 2.1.4
- [ ] 1.2.3
- [ ] 5.4

### Solution

```
spark.version
```

```
'3.3.2'
```

### Question 2:

**HVFHW June 2021**

Read it with Spark using the same schema as we did in the lessons. We will use this dataset for all the remaining questions.  Repartition it to 12 partitions and save it to parquet.
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB). Select the answer which most closely matches.

- [ ] 2 MB
- [x] 24 MB
- [ ] 100 MB
- [ ] 250 MB

### Solution:
```
df = spark.sql("""SELECT * FROM fhvhv""")

df.repartition(12)\
    .write\
    .option("compression", "snappy")\
    .mode("overwrite")\
    .parquet("/tmp/dtc/fhvhv-week5")
```

```
ls -lh /tmp/dtc/fhvhv-w5q2/

-rw-r--r--@ 1 iobruno  wheel     0B Mar  5 00:08 _SUCCESS
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00000-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00001-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00002-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00003-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00004-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00005-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00006-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00007-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00008-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00009-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00010-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel    24M Mar  5 00:08 part-00011-f51983be-cec6-40ed-bc3f-198e2cfa39ac-c000.snappy.parquet
```

## Question 3:

**Count records**

How many taxi trips were there on June 15? Consider only trips that started on June 15.

- [ ] 308,164
- [ ] 12,856
- [X] 452,470
- [ ] 50,982

### Solution:
```sql
spark.sql("""

    SELECT
        dayofmonth(pickup_datetime) as day_of_month,
        count(1) as num_trips
    FROM
        fhvhv
    WHERE
        dayofmonth(pickup_datetime) = 15
    GROUP BY
        dayofmonth(pickup_datetime)

""").take(1)
```

-- Result:
```
[Row(day_of_month=15, num_trips=452470)]
```

## Question 4:

**Longest trip for each day**

Now calculate the duration for each trip. How long was the longest trip in Hours?

- [X] 66.87 Hours
- [ ] 243.44 Hours
- [ ] 7.68 Hours
- [ ] 3.32 Hours

### Solution:
```sql
spark.sql("""

    WITH tripdata AS (
        SELECT
            pickup_location_id,
            dropoff_location_id,
            pickup_datetime,
            dropoff_datetime,
            (CAST(dropoff_datetime as LONG) - CAST(pickup_datetime as LONG)) as duration_in_secs
        FROM
            fhvhv
    ),

    trip_duration AS (
        SELECT
            (duration_in_secs/3600) as duration_in_hours,
            dense_rank() OVER( ORDER BY duration_in_secs DESC ) as rnk
        FROM tripdata t
    )

    SELECT
        td.duration_in_hours
    FROM trip_duration td
    WHERE td.rnk = 1

""").take(1)
```

```
[Row(duration_in_hours=66.8788888888889)]
```

### Question 5:

**User Interface**

 Spark’s User Interface which shows application's dashboard runs on which local port?

- [ ] 80
- [ ] 443
- [X] 4040
- [ ] 8080

### Solution:

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.3.2
      /_/

Using Python version 3.9.12 (main, Apr  5 2022 01:52:34)

Spark context Web UI available at http://magi:4040

Spark context available as 'sc' (master = local[*], app id = local-1677421297685).
SparkSession available as 'spark'.
```

### Question 6:

**Most frequent pickup location zone**

Load the zone lookup data into a temp view in Spark
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the fhvhv June 2021 data, what is the name of the most frequent pickup location zone?

- [ ] East Chelsea
- [ ] Astoria
- [ ] Union Sq
- [x] Crown Heights North

### Solution

```sql
spark.sql("""

    WITH trip_count_per_location AS (
        SELECT
            f.pickup_location_id,
            count(1) as num_trips,
            dense_rank() over (order by count(1) desc) as rnk
        FROM fhvhv f
        GROUP BY f.pickup_location_id
    )

    SELECT
        t.pickup_location_id,
        z.zone,
        t.num_trips,
        t.rnk
    FROM trip_count_per_location t
    INNER JOIN zones z ON t.pickup_location_id = z.location_id
    WHERE t.rnk = 1

""").take(1)
```

```
[Row(pickup_location_id=61, zone='Crown Heights North', num_trips=231279, rnk=1)]
```


## Submitting the solutions

* Form for submitting: https://forms.gle/EcSvDs6vp64gcGuD8
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 06 March (Monday), 22:00 CET
