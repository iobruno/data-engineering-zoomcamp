## Week 5 Homework 

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the FHV 2019-10 data found here. [FHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz)


**Question 1: Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
```python
spark.version
'3.5.0'
```


**Question 2:** Read the **October 2019 FHV data** into a Spark Dataframe with a schema as we did in the lessons and repartition the Dataframe to 6 partitions, followed by saving it to parquet. 

What is the average size (in MB) of the parquet files that were created? Select the answer which most closely matches.
- [ ] 1 MB
- [x] 6 MB
- [ ] 25 MB
- [ ] 87 MB

```python
df = spark.sql("""SELECT * FROM fhv""")
df.repartition(6)\
    .write\
    .mode("overwrite")\
    .parquet("/tmp/dtc-homework/fhv/")
```
```shell
ls -lh /tmp/dtc-homework/fhv/

total 76768
-rw-r--r--@ 1 iobruno  wheel     0B Mar  1 13:01 _SUCCESS
-rw-r--r--@ 1 iobruno  wheel   6.3M Mar  1 13:01 part-00000-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel   6.2M Mar  1 13:01 part-00001-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel   6.2M Mar  1 13:01 part-00002-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel   6.2M Mar  1 13:01 part-00003-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel   6.2M Mar  1 13:01 part-00004-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
-rw-r--r--@ 1 iobruno  wheel   6.2M Mar  1 13:01 part-00005-83f7a6b5-f525-418c-8ecb-b125533cee70-c000.snappy.parquet
```


**Question 3: How many taxi trips were there on the 15th of October?**

Note: consider only trips that started on the 15th of October.
- [ ] 108,164
- [ ] 12,856
- [ ] 452,470
- [x] 62,610

```python
spark.sql("""
    with trips_per_month_day AS (
        select
            month(pickup_datetime) as month,
            dayofmonth(pickup_datetime) as day, 
            count(1) as num_trips
        from
            fhv
        group by 
            month(pickup_datetime), 
            dayofmonth(pickup_datetime)
    )

    select * 
    from trips_per_month_day 
    where 
        month = 10 
        and day = 15
""").take(1)
```
```
[Row(month=10, day=15, num_trips=62610)]
```


**Question 4: What is the length of the longest trip in the dataset in hours?** 
- [x] 631,152.50 Hours
- [ ] 243.44 Hours
- [ ] 7.68 Hours
- [ ] 3.32 Hours

```python
spark.sql("""
    with trip_records AS (
        select
            pickup_location_id,
            dropoff_location_id,
            pickup_datetime,
            dropoff_datetime,
            (cast(dropoff_datetime as long) - cast(pickup_datetime as long))/3600 as duration_in_hours
        from 
            fhv
    )

    select 
        duration_in_hours,
        dense_rank() over (order by duration_in_hours desc) as rnk
    from
        trip_records t

""").take(1)
```
```
[Row(duration_in_hours=631152.5, rnk=1)]
```


**Question 5: The Spark’s UI, which shows the application's dashboard, runs on what local port?**
- [ ] 80
- [ ] 443
- [x] 4040
- [ ] 8080


**Question 6: Least frequent pickup location zone?**

Load the zone lookup data into a temp view in Spark
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?</br>

- [ ] East Chelsea
- [x] Jamaica Bay
- [ ] Union Sq
- [ ] Crown Heights North

```python
spark.sql("""
    with trips_per_location AS (
        select
            pickup_location_id,
            count(1) as num_trips,
            dense_rank() over (order by count(1) asc) as rnk
        from
            fhv
        group by
            pickup_location_id
    )

    select
        pu.zone,
        t.num_trips,
        t.rnk
    from
        trips_per_location t
    inner join
        zones pu on t.pickup_location_id = pu.location_id
    where
        rnk = 1
""").take(1)
```

```
[Row(zone='Jamaica Bay', num_trips=1, rnk=1)]
```

## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw5
- Deadline: See the website