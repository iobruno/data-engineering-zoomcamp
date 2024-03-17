
# Stream processing with RisingWave

[Documentation](https://docs.risingwave.com/) 📑 [Tutorials](https://tutorials.risingwave.com/) 🎯 [RisingWave Cloud](https://cloud.risingwave.com/) 🚀 [Get Instant Help](https://risingwave.com/slack)


In this hands-on workshop, we’ll learn how to process real-time streaming data using SQL in RisingWave. The system we’ll use is [RisingWave](https://github.com/risingwavelabs/risingwave), an open-source SQL database for processing and managing streaming data. You may not feel unfamiliar with RisingWave’s user experience, as it’s fully wire compatible with PostgreSQL.

![RisingWave](https://raw.githubusercontent.com/risingwavelabs/risingwave-docs/main/docs/images/new_archi_grey.png)

We’ll cover the following topics in this Workshop:
- Why Stream Processing?
- Stateless computation (Filters, Projections)
- Stateful Computation (Aggregations, Joins)
- Time windowing
- Watermark
- Data Ingestion and Delivery

RisingWave in 10 Minutes: https://tutorials.risingwave.com/docs/intro

Project Repo: [RisingWave Labs](https://github.com/risingwavelabs/risingwave-data-talks-workshop-2024-03-04)


## Homework

**Question 0:** What are the dropoff taxi zones at the latest dropoff times ?

_This question is just a warm-up to introduce dynamic filter, please attempt it before viewing its solution._ 

For this part, we will use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/).


**Question 1:** Create a materialized view to compute the average, min and max trip time between each taxi zone.

Note that we consider the do not consider `a->b` and `b->a` as the same trip pair.
So as an example, you would consider the following trip pairs as different pairs:
```plaintext
Yorkville East -> Steinway
Steinway -> Yorkville East
```

From this MV, find the pair of taxi zones with the highest average trip time.
You may need to use the [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/) for this.

**Bonus (no marks)**: Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute, but the max trip time is 10 minutes and 20 minutes respectively.

Options:
- [x] Yorkville East, Steinway
- [ ] Murray Hill, Midwood
- [ ] East Flatbush/Farragut, East Harlem North
- [ ] Midtown Center, University Heights/Morris Heights

```sql
-- Answer for Q1 and Q2
create materialized view if not exists trip_duration_per_zone as
with trip_duration as (
    select
        puz.zone as pickup_zone,
        doz.zone as dropoff_zone,
        (tpep_dropoff_datetime - tpep_pickup_datetime) as duration
    from
        trip_data ytt
    inner join
        taxi_zone puz on ytt.pulocationid = puz.location_id
    inner join
        taxi_zone doz on ytt.dolocationid = doz.location_id
)

select
    pickup_zone,
    dropoff_zone,
    count(1)        as num_trips,
    avg(duration)   as avg_duration,
    min(duration)   as shortest_trip,
    max(duration)   as longest_trip
from
    trip_duration
group by
    pickup_zone,
    dropoff_zone;
```

```sql
select * from trip_duration_per_zone
order by avg_duration desc
limit 1;
```

| pickup_zone    | dropoff_zone | num_trips | avg_duration               |
| :------------- | :----------- | --------: | :------------------------- |
| Yorkville East | Steinway     | 1         | 23 hours 59 mins 33.0 secs |


**Question 2:** Recreate the MV(s) in question 1, to also find the **number of trips** for the pair of taxi zones with the highest average trip time.
- [ ] 5
- [ ] 3
- [ ] 10
- [x] 1


**Question 3:** From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups?

For example if the latest pickup time is 2020-01-01 12:00:00,
then the query should return the top 3 busiest zones from 2020-01-01 11:00:00 to 2020-01-01 12:00:00.

HINT: You can use [dynamic filter pattern](https://docs.risingwave.com/docs/current/sql-pattern-dynamic-filters/)
to create a filter condition based on the latest pickup time.

NOTE: For this question `17 hours` was picked to ensure we have enough data to work with.

Options:
- [ ] Clinton East, Upper East Side North, Penn Station
- [x] LaGuardia Airport, Lincoln Square East, JFK Airport
- [ ] Midtown Center, Upper East Side South, Upper East Side North
- [ ] LaGuardia Airport, Midtown Center, Upper East Side North

```sql
create materialized view if not exists busiest_zones_last_17h_since_last as
select
    tz.zone as pickup_zone,
    count(1) as num_trips
from
    trip_data ytt
join
    taxi_zone tz on ytt.pulocationid = tz.location_id
where
    ytt.tpep_pickup_datetime >= (select max(tpep_pickup_datetime) - interval '17 hours' from trip_data)
group by
    tz.zone;
```

```sql
select *
from busiest_zones_last_17h_since_last
order by num_trips desc;
```

| pickup_zone         | num_trips |
| :------------------ | --------: |
| LaGuardia Airport   | 19        |
| JFK Airport         | 17        |
| Lincoln Square East | 17        |


## Submitting the solutions
- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/workshop2
- Deadline: 18 March (Monday), 23:00 CET

## Rewards 🥳
Everyone who completes the homework will get a pen and a sticker, and 5 lucky winners will receive a Tshirt and other secret surprises!  
We encourage you to share your achievements with this workshop on your socials and look forward to your submissions 😁

- Follow us on **LinkedIn**: https://www.linkedin.com/company/risingwave
- Follow us on **GitHub**: https://github.com/risingwavelabs/risingwave
- Join us on **Slack**: https://risingwave-labs.com/slack

See you around!


## Extra

**Extra 1**: What is RisingWave meant to be used for?
- [ ] OLTP workloads
- [ ] Adhoc
- [ ] OLAP Workloads
- [x] Stream Processing


**Extra 2**: What is the interface which RisingWave supports?
- [ ] Java SDK
- [x] PostgreSQL like interface
- [ ] Rust SDK
- [ ] Python SDK


**Extra 3**: What if I want to run a custom function which RisingWave does not support?
- [ ] Sink the data out, run the function, and sink it back in
- [x] Write a Python / Java / WASM / JS UDF

Ref.: https://docs.risingwave.com/docs/current/user-defined-functions/


**Extra 4**: Is this statement True or False?
> I cannot create materialized views on top of other materialized views
- [ ] True
- [x] False


**Extra 5**: How does RisingWave process ingested data?
- [ ] Incrementally, only on checkpoints
- [ ] In batch, each time a user queries a materialized view
- [ ] In batch, at fixed intervals
- [ ] Incrementally, as new records are ingested


**Extra 6**: Is the following Statement True or False:
> RisingWave is only for Stream Processing, it cannot serve any select requests from applications
- [ ] True
- [x] False


**Extra 7**: Why can’t we use cross joins in RisingWave Materialized Views?
- [ ] Because they are not supported by the SQL standard.
- [ ] Because they are not supported by the Incremental View Maintenance algorithm.
- [ ] Because they are not supported by the PostgreSQL planner.
- [ ] Because they are too expensive, so it is banned in RisingWave’s stream engine.


**Extra 8**: What is the recommended way to view the progress of long-running SQL statements like `CREATE MATERIALIZED VIEW` in RisingWave?
- [ ] Using the EXPLAIN ANALYZE statement
- [ ] Querying the `rw_catalog.rw_ddl_progress` table
- [ ] Checking the RisingWave logs
- [ ] It is not possible to view the progress of such statements


**Extra 9**: How do I view the execution plan of my SQL query?
- [ ] `SHOW <query>`
- [x] `EXPLAIN <query>`
- [ ] `DROP <query>`
- [ ] `VIEW <query>`


**Extra 10**: Which is used to ingest data from external systems?
- [x] `CREATE SOURCE <...>`
- [ ] `CREATE SINK <...>`


**Extra 11**: What is the purpose of a watermark?
- [ ] To specify the time at which a record was ingested
- [ ] To specify the time at which a record was updated
- [ ] To specify the time at which a record was deleted
- [ ] To specify the time at which a record is considered stale, and can be deleted
