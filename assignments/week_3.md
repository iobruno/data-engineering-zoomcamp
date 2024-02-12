## Week 3 Homework

**Important Note:**
For this homework we will be using the Green Taxi Trip Record Parquet files from the New York City Taxi Data found here:  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page  

If you are using orchestration such as Mage, Airflow or Prefect do not load the data into Big Query using the orchestrator. Stop with loading the files into a bucket.  

**NOTE:** You will need to use the PARQUET option files when creating an External Table

**SETUP:**
- Create an external table using the Green Taxi Trip Records Data for 2022 data.  
- Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table).


## Question 1
What is count of records for the 2022 Green Taxi Data ?
- [ ] 65,623,481
- [x] 840,402
- [ ] 1,936,423
- [ ] 253,647

```sql
select 
  count(1) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.ext_green`
```


## Question 2
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- [x] 0 MB for the External Table and 6.41MB for the Materialized Table
- [ ] 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- [ ] 0 MB for the External Table and 0MB for the Materialized Table
- [ ] 2.14 MB for the External Table and 0MB for the Materialized Table

```sql
-- External Table (0 Bytes)
select 
  count(distinct(PULocationID)) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.ext_green`
```

```sql
-- Materialized Table (6.41 MB)
select 
  count(distinct(PULocationID)) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.green`
```


## Question 3
How many records have a fare_amount of 0 ?
- [ ] 12,488
- [ ] 128,219
- [ ] 112
- [x] 1,622

```sql
select 
  count(1) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.green` g
where 
  g.fare_amount = 0
```

## Question 4
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime?
- [ ] Cluster on lpep_pickup_datetime Partition by PUlocationID
- [x] Partition by lpep_pickup_datetime Cluster on PUlocationID
- [ ] Partition by lpep_pickup_datetime and Partition by PUlocationID
- [ ] Cluster on by lpep_pickup_datetime and Cluster on PUlocationID

## Question 5
Write a query to retrieve the distinct PULocationID between `lpep_pickup_datetime`
06/01/2022 and 06/30/2022 (`inclusive`)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

- [ ] 22.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- [x] 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
- [ ] 5.63 MB for non-partitioned table and 0 MB for the partitioned table
- [ ] 10.31 MB for non-partitioned table and 10.31 MB for the partitioned table

```sql
-- Unpartitioned Table Query (12.82 MB)
select 
  distinct(g.PULocationID) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.green_unpartitioned` g
where
  date_trunc(g.lpep_pickup_datetime, DAY) between '2022-06-01' and '2022-06-30'
```

```sql
-- Partitioned Table Query (1.12 MB)
select 
  distinct(g.PULocationID) as num_records
from 
  `iobruno-gcp-labs.raw_nyc_tlc.green` g
where
  date_trunc(g.lpep_pickup_datetime, DAY) between '2022-06-01' and '2022-06-30'
```


## Question 6
Where is the data stored in the External Table you created ?
- [ ] Big Query
- [x] GCP Bucket
- [ ] Big Table
- [ ] Container Registry


## Question 7
It is best practice in Big Query to always cluster your data?
- [ ] True
- [x] False

```text
Not under the following conditions:
- If the dataset is too small
- If the data is often updated where if the columns being used are not immutable
```

## (Bonus: Not worth points) Question 8
No Points: Write a SELECT count(*) query FROM the materialized table you created.

How many bytes does it estimate will be read ? Why ?

Note: Column types for all files used in an External Table must have the same datatype. While an External Table may be created and shown in the side panel in Big Query, this will need to be validated by running a count query on the External Table to check if any errors occur. 
 
## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw3