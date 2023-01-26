# Data Engineering Zoomcamp Homework - Week 1 Part A

In this homework we'll prepare the environment
and practice with Docker and SQL

## Question 1. Knowing docker tags

Run the command to get information on Docker

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file*

- [ ] `--imageid string`
- [X] `--iidfile string`
- [ ] `--idimage string`
- [ ] `--idfile string`

### Solution:
```bash
$ docker build --help | grep -i "Write the image ID to the file"

      --iidfile string          Write the image ID to the file
```

## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list).
How many python packages/modules are installed?

- [ ] 1
- [ ] 6
- [X] 3
- [ ] 7

### Solution:

```bash
$ docker run -it --entrypoint bash python:3.9

root@9788a4a17084:/# pip list

Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4

WARNING: You are using pip version 22.0.4; however, version 22.3.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
```

## Question 3. Count records

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- [ ] 20689
- [X] 20530
- [ ] 17630
- [ ] 21090

### Solution:

```sql
select
    count(1) as taxi_trips
from 
    ntl_green_taxi
where
    date_trunc('day', lpep_pickup_datetime) = '2019-01-15'
    and date_trunc('day', lpep_dropoff_datetime) = '2019-01-15';
```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance Use the pick up time for your calculations.

- [ ] 2019-01-18
- [ ] 2019-01-28
- [X] 2019-01-15
- [ ] 2019-01-10

### Solution:

```sql
with ranked_trip_distances as (
    select
        date_trunc('day', lpep_pickup_datetime) as pickup_day,
        max(trip_distance)                      as max_trip_distance,
        dense_rank() over (order by max(trip_distance) desc) as ranking
    from
        ntl_green_taxi
    group by
        date_trunc('day', lpep_pickup_datetime)
)

select pickup_day
from ranked_trip_distances td
where td.ranking = 1;
```


## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?

- [ ] 2: 1282 ; 3: 266
- [ ] 2: 1532 ; 3: 126
- [X] 2: 1282 ; 3: 254
- [ ] 2: 1282 ; 3: 274

### Solution:

```sql
select
    passenger_count,
    count(1) as trips
from
    ntl_green_taxi t
where
    date_trunc('day', lpep_pickup_datetime) = '2019-01-01'
    and t.passenger_count between 2 and 3
group by
    t.passenger_count;
```

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- [ ] Central Park
- [ ] Jamaica
- [ ] South Ozone Park
- [X] Long Island City/Queens Plaza

### Solution:

```sql
WITH trips_from_astoria_rnked_by_tip_amount as (
    select
        t."DOLocationID" as dropoff_location_id,
        max(tip_amount) as largest_tip,
        dense_rank() over (order by max(tip_amount) desc) as rnk
    from ntl_green_taxi t
    inner join ntl_lookup_zones z on (
        t."PULocationID" = z."LocationID" and
        z."Zone" = 'Astoria'
    )
    group by
        t."DOLocationID"
)

select
    t.dropoff_location_id,
    z."Zone" as zone_name
from
    trips_from_astoria_rnked_by_tip_amount t
inner join
    ntl_lookup_zones z on t.dropoff_location_id = z."LocationID"
where
    t.rnk = 1;
```

## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 26 January (Thursday), 22:00 CET


## Solution

We will publish the solution here