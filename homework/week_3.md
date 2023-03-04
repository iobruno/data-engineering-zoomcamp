## Week 3 Homework
**Important Note:**

You can load the data however you would like, but keep the files in .GZ Format.
If you are using orchestration such as Airflow or Prefect do not load the data into Big Query using the orchestrator.</br>
Stop with loading the files into a bucket. </br></br>

**NOTE:**
- You can use the CSV option for the GZ files when creating an External Table</br>

**SETUP:**
- Create an external table using the fhv 2019 data. </br>
- Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
- Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

## Question 1:
What is the count for fhv vehicle records for year 2019?
- [ ] 65,623,481
- [x] 43,244,696
- [ ] 22,978,333
- [ ] 13,942,414

### Solution:

```sql
-- Query Result: 43244696
SELECT
  COUNT(1) as records
FROM
  `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata` fhv;
```

## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.</br>
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- [ ] 25.2 MB for the External Table and 100.87MB for the BQ Table
- [ ] 225.82 MB for the External Table and 47.60MB for the BQ Table
- [ ] 0 MB for the External Table and 0MB for the BQ Table
- [x] 0 MB for the External Table and 317.94MB for the BQ Table

### Solution:

```sql
-- Scans for 317.94 MB on BQ Table:
SELECT
    COUNT(DISTINCT(Affiliated_base_number)) as records
FROM
    `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata` fhv;
```

```sql
-- Scans for 0 B on BQ Table:
SELECT
    COUNT(DISTINCT(Affiliated_base_number)) as records
FROM
    `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata_ext_csv_gz` fhv;
```

**BQ Internal Table (from .csv.gz)**:
![bigquery-internal-from-csv](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week3_bq_internal.png)

**BQ External Table (from .csv.gz)**:
![bigquery-external-from-csv](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week3_bq_external.png)


## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
- [x] 717,748
- [ ] 1,215,687
- [ ] 5
- [ ] 20,332

### Solution:
```sql
-- Query Result: 717748
SELECT
    COUNT(1) as records
FROM
    `iobruno-data-eng-zoomcamp.dtc_dw_staging.nyc_fhv_tripdata` fhv
WHERE
    fhv.PUlocationID IS NULL
    AND fhv.DOlocationID IS NULL;
```

## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

- [ ] Cluster on pickup_datetime Cluster on affiliated_base_number
- [x] Partition by pickup_datetime Cluster on affiliated_base_number
- [ ] Partition by pickup_datetime Partition by affiliated_base_number
- [ ] Partition by affiliated_base_number Cluster on pickup_datetime

```text
- Partitions reduces the amount that BigQuery has to processes to fetch the results.
Instead of doing a FULL table scan to match each result, it can just look up for the results
within the partitions.

- Clustering, on the other hand, clusters or groups togethers the entries based on a specified column,
which helps boosting the query performance (and costs) when the results are ordered by that specific column
```

## Question 5:
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number
between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).

Use the BQ table you created earlier in your from clause and note the estimated bytes.

Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated
bytes processed. What are these values? Choose the answer which most closely matches.

- [ ] 12.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- [x] 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table
- [ ] 582.63 MB for non-partitioned table and 0 MB for the partitioned table
- [ ] 646.25 MB for non-partitioned table and 646.25 MB for the partitioned table

### Solution:

** Partition the table**:
```sql
-- Scans for 647.87 MB
CREATE OR REPLACE TABLE `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata_by_date`
PARTITION BY DATE(pickup_datetime) AS (
    SELECT *
    FROM `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata`
);
```

**Non-partitioned Table - Query Consumption**: 647.87 MB
```sql
-- Scans for 23.05 MB
SELECT
  DISTINCT(Affiliated_base_number)
FROM
  `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata` fhv
WHERE
  fhv.pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';
```

**Partitioned Table - Query Consumption**: 23.05 MB
```sql
SELECT
  DISTINCT(Affiliated_base_number)
FROM
  `iobruno-data-eng-zoomcamp.dtc_dw_staging.fhv_tripdata_by_date` fhv
WHERE
  fhv.pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';
```

## Question 6:
Where is the data stored in the External Table you created?

- [ ] Big Query
- [x] GCP Bucket
- [ ] Container Registry
- [ ] Big Table


## Question 7:
It is best practice in Big Query to always cluster your data:

- [ ] True
- [x] False

### Solution:

- Best practises efforts are generally put in practice to either improve Query Performance or reduce Costs
- However, on tables where the data size < 1 GB, Clustering or Partitioning might actually incur in worsening the performance,
as there'll be more metadata processing and lookups involved in the Query Plan

## (Not required) Question 8:
A better format to store these files may be parquet. Create a data pipeline to download the gzip files
and convert them into parquet. Upload the files to your GCP Bucket and create an External and BQ Table.

Note: Column types for all files used in an External Table must have the same datatype. While an External Table may be created and shown in the side panel in Big Query, this will need to be validated by running a count query on the External Table to check if any errors occur.

![bigquery-parquet-snappy-gzip-csv](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week3_bq_parquet_csv.png)

## Submitting the solutions

* Form for submitting: https://forms.gle/rLdvQW2igsAT73HTA
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 13 February (Monday), 22:00 CET


## Solution

We will publish the solution here
