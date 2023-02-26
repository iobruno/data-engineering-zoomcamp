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
Python 3.9.12 (main, Apr  5 2022, 01:52:34)
[Clang 12.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
23/02/26 11:21:37 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
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
>>>

>>> spark.version
'3.3.2'
```



### Question 2: 

**HVFHW June 2021**

Read it with Spark using the same schema as we did in the lessons. We will use this dataset for all the remaining questions.  Repartition it to 12 partitions and save it to parquet.  
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB). Select the answer which most closely matches.  

- [ ] 2 MB
- [ ] 24 MB
- [ ] 100 MB
- [ ] 250 MB


### Question 3: 

**Count records**  

How many taxi trips were there on June 15? Consider only trips that started on June 15.

- [ ] 308,164
- [ ] 12,856
- [ ] 452,470
- [ ] 50,982


### Question 4: 

**Longest trip for each day**  

Now calculate the duration for each trip. How long was the longest trip in Hours?

- [ ] 66.87 Hours
- [ ] 243.44 Hours
- [ ] 7.68 Hours
- [ ] 3.32 Hours


### Question 5: 

**User Interface**

 Spark’s User Interface which shows application's dashboard runs on which local port?

- [ ] 80
- [ ] 443
- [ ] 4040
- [ ] 8080


### Question 6: 

**Most frequent pickup location zone**

Load the zone lookup data into a temp view in Spark
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)

Using the zone lookup data and the fhvhv June 2021 data, what is the name of the most frequent pickup location zone?

- East Chelsea
- Astoria
- Union Sq
- Crown Heights North


## Submitting the solutions

* Form for submitting: https://forms.gle/EcSvDs6vp64gcGuD8
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 06 March (Monday), 22:00 CET


## Solution

We will publish the solution here