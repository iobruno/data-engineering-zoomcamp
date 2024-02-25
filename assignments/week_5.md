## Week 5 Homework 

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the FHV 2019-10 data found here. [FHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz)

**Question 1: Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)


**Question 2:** Read the **October 2019 FHV data** into a Spark Dataframe with a schema as we did in the lessons and repartition the Dataframe to 6 partitions, followed by saving it to parquet. 

What is the average size (in MB) of the parquet files that were created? Select the answer which most closely matches.
- [ ] 1 MB
- [ ] 6 MB
- [ ] 25 MB
- [ ] 87 MB

**Question 3: How many taxi trips were there on the 15th of October?**

Note: consider only trips that started on the 15th of October.
- [ ] 108,164
- [ ] 12,856
- [ ] 452,470
- [ ] 62,610

> [!IMPORTANT]
> Be aware of columns order when defining schema

**Question 4: What is the length of the longest trip in the dataset in hours?** 
- [ ] 631,152.50 Hours
- [ ] 243.44 Hours
- [ ] 7.68 Hours
- [ ] 3.32 Hours

**Question 5: The Spark’s UI, which shows the application's dashboard, runs on what local port?**
- [ ] 80
- [ ] 443
- [ ] 4040
- [ ] 8080

**Question 6: Least frequent pickup location zone?**

Load the zone lookup data into a temp view in Spark
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?</br>

- [ ] East Chelsea
- [ ] Jamaica Bay
- [ ] Union Sq
- [ ] Crown Heights North


## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw5
- Deadline: See the website