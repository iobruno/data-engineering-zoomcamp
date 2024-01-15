## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits*

- [ ] `--delete`
- [ ] `--rc`
- [ ] `--rmc`
- [x] `--rm`


## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ).

```shell
docker run -it --entrypoint bash python:3.9
```

What is version of the package *wheel* ?

- [x] 0.42.0
- [ ] 1.0.0
- [ ] 23.0.1
- [ ] 58.1.0

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- [ ] 15767
- [x] 15612
- [ ] 15859
- [ ] 89009

Answer:
```sql
with green_tripdata as (
    select
      date_trunc('day', g.lpep_pickup_datetime)  as pickup_date,
      date_trunc('day', g.lpep_dropoff_datetime) as dropoff_date,
      g.*
    from green_taxi_data g
)

select
    pickup_date,
    dropoff_date,
    count(1) as num_trips
from
    green_tripdata
where
    pickup_date >= '2019-09-18' and
    dropoff_date < '2019-09-19'
group by
    pickup_date, 
    dropoff_date;
```


## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- [ ] 2019-09-18
- [ ] 2019-09-16
- [x] 2019-09-26
- [ ] 2019-09-21

```sql
with green_tripdata as (
    select
        date_trunc('day', g.lpep_pickup_datetime)  as pickup_date,
        date_trunc('day', g.lpep_dropoff_datetime) as dropoff_date,
        g.*
    from green_taxi_data g
)

select
    pickup_date,
    max(trip_distance) as max_trip_distance
from
    green_tripdata
group by
    pickup_date
order by
    max_trip_distance desc
```


## Question 5. The number of passengers

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

- [x] "Brooklyn" "Manhattan" "Queens"
- [ ] "Bronx" "Brooklyn" "Manhattan"
- [ ] "Bronx" "Manhattan" "Queens"
- [ ] "Brooklyn" "Queens" "Staten Island"

```sql
with green_tripdata as (
    select
        date_trunc('day', g.lpep_pickup_datetime)  as pickup_date,
        g.*
    from green_taxi_data g
),

overall_amount_per_borough as (
    select
        z.borough,
        g.pickup_date,
        sum(g.total_amount)::numeric as overall_amount,
        rank() over (order by sum(g.total_amount) desc) as rnk
    from
        green_tripdata g
    left join
        zone_lookup z ON g.pu_location_id = z.location_id
    where
        g.pickup_date = '2019-09-18' and
        z.borough != 'Unknown'
    group by
        g.pickup_date,
        z.borough
    order by
        overall_amount desc
)

select *
from  overall_amount_per_borough
where overall_amount > 50000 and rnk < 4
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- [ ] Central Park
- [ ] Jamaica
- [x] JFK Airport
- [ ] Long Island City/Queens Plaza

```sql
with green_tripdata as (
    select
        date_trunc('month', g.lpep_pickup_datetime)  as pickup_month,
        g.*
    from green_taxi_data g
),

largest_tip_per_dropoff_zone as (
    select
        pz.zone as pickup_zone,
        dz.zone as dropoff_zone,
        max(g.tip_amount) as largest_tip,
        dense_rank() over (order by max(tip_amount) desc) as rnk
    from
        green_tripdata g
    inner join
        zone_lookup pz ON g.pu_location_id = pz.location_id
    inner join
        zone_lookup dz ON g.do_location_id = dz.location_id
    where
        g.pickup_month = '2019-09-01' and
        pz.zone = 'Astoria'
    group by
        pz.zone,
        dz.zone
)

select * from largest_tip_per_dropoff_zone
where rnk = 1;
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

```shell
❯ tf apply -auto-approve        

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.stg_nyc_dataset will be created
  + resource "google_bigquery_dataset" "stg_nyc_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "raw_nyc_trip_record_data"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "us-central1"
      + max_time_travel_hours      = (known after apply)
      + project                    = "iobruno-gcp-labs"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.iobruno_lakehouse_raw will be created
  + resource "google_storage_bucket" "iobruno_lakehouse_raw" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US-CENTRAL1"
      + name                        = "iobruno-lakehouse-raw"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }
          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.
google_bigquery_dataset.stg_nyc_dataset: Creating...
google_storage_bucket.iobruno_lakehouse_raw: Creating...
google_bigquery_dataset.stg_nyc_dataset: Creation complete after 1s [id=projects/iobruno-gcp-labs/datasets/raw_nyc_trip_record_data]
google_storage_bucket.iobruno_lakehouse_raw: Creation complete after 2s [id=iobruno-lakehouse-raw]
Releasing state lock. This may take a few moments...

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET