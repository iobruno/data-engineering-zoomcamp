## Week 2 Homework

The goal of this homework is to familiarise users with workflow orchestration and observation.


## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

- [x] * 447,770
- [ ] * 766,792
- [ ] * 299,234
- [ ] * 822,132

### Solution:
```
13:37:55.601 | INFO    | prefect.engine - Created flow run 'original-serval' for flow 'NYC Green Taxi CSV Dataset to GCS'
13:37:55.651 | INFO    | Flow run 'original-serval' - Fetching URL Datasets from .yml
13:37:55.666 | INFO    | Flow run 'original-serval' - Created task run 'fetch_csv_from-0' for task 'fetch_csv_from'
13:37:55.666 | INFO    | Flow run 'original-serval' - Executing 'fetch_csv_from-0' immediately...
13:37:55.682 | INFO    | Task run 'fetch_csv_from-0' - Now fetching: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz
13:37:56.218 | INFO    | Task run 'fetch_csv_from-0' - Finished in state Completed()
13:37:56.228 | INFO    | Flow run 'original-serval' - Created task run 'save_to_fs_with-0' for task 'save_to_fs_with'
13:37:56.228 | INFO    | Flow run 'original-serval' - Executing 'save_to_fs_with-0' immediately...

13:38:03.710 | INFO    | Task run 'save_to_fs_with-0' - Dataset contains: 447770 lines

13:38:03.720 | INFO    | Task run 'save_to_fs_with-0' - Finished in state Completed()
13:38:03.730 | INFO    | Flow run 'original-serval' - Created task run 'load_into_gcs_with-0' for task 'load_into_gcs_with'
13:38:03.730 | INFO    | Flow run 'original-serval' - Executing 'load_into_gcs_with-0' immediately...
13:38:03.828 | INFO    | Task run 'load_into_gcs_with-0' - Getting bucket 'iobruno_dtc_datalake_raw'.
13:38:04.322 | INFO    | Task run 'load_into_gcs_with-0' - Uploading from PosixPath('/Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/datasets/green_tripdata_2020-01.csv.gz') to the bucket 'iobruno_dtc_datalake_raw' path 'green_taxi/green_tripdata_2020-01.csv.gz'.
13:38:05.747 | INFO    | Task run 'load_into_gcs_with-0' - Finished in state Completed()
13:38:05.762 | INFO    | Flow run 'original-serval' - Finished in state Completed('All states completed.')
```

## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows.

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

- [x] `0 5 1 * *`
- [ ] `0 0 5 1 *`
- [ ] `5 * 1 0 *`
- [ ] `* * 5 1 0`

### Solution:

```
$ prefect deployment build flows/flow_web_csv_dataset_to_gcs.py:ingest -n day01-monthly-csv-to-gcs --cron "0 5 1 * * " -a


prefect deployment build flows/flow_web_csv_dataset_to_gcs.py:ingest -n every-minute --cron "* * * * * " -a

Found flow 'NYC Taxi Trip data CSV Dataset to GCS'
Default '.prefectignore' file written to /Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/.prefectignore
Deployment YAML created at '/Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/ingest-deployment.yaml'.
Deployment storage None does not have upload capabilities; no files uploaded.  Pass --skip-upload to suppress this warning.
Deployment 'NYC Taxi Trip data CSV Dataset to GCS/day01-monthly-csv-to-gcs' successfully created with id 
'00d1d042-7d4d-412a-82a5-beed75380d25'.

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
```

## Question 3. Loading data to BigQuery

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. 
This new script should not fill or remove rows with missing values. 
(The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. 
Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color.

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. 
Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- [x] 14,851,920
- [ ] 12,282,990
- [ ] 27,235,753
- [ ] 11,338,483

### Solution:
```sql
select count(1) as counter 
from `iobruno-data-eng-zoomcamp.dtc_dw_staging.yellow_tripdata`  where true
```
```Result:
| Row | counter  |
|-----|----------|
| 1   | 14851920 |
```


## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. 
Prefect can look in the GitHub repo to find your flow code and read it. 
Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image.

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- [ ] 88,019
- [ ] 192,297
- [x] 88,605
- [ ] 190,225

### Solution:
```bash
$ prefect deployment build flows/flow_web_csv_dataset_to_gcs.py:ingest --name git-prefect-flow -sb github/prefect-github-integration -a

Found flow 'NYC GCS  to BigQuery'
Default '.prefectignore' file written to /Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/.prefectignore
Deployment YAML created at '/Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/ingest-deployment.yaml'.
Deployment storage GitHub(repository='https://github.com/DataTalksClub/data-engineering-zoomcamp.git', reference=None, 
access_token=None, include_git_objects=True) does not have upload capabilities; no files uploaded.  Pass --skip-upload to suppress 
this warning.
Deployment 'NYC GCS  to BigQuery/git-prefect-flow' successfully created with id 'b6e0074b-fa9d-406a-8510-8ecc9f1d8fc6'.

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
```


## Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur.

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up.

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook.

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days.

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create.


How many rows were processed by the script?

- [ ] `125,268`
- [ ] `377,922`
- [ ] `728,390`
- [x] `514,392`

### Solution:

```
7:14:45.338 | INFO    | prefect.engine - Created flow run 'rousing-sawfly' for flow 'NYC Taxi Trip data CSV Dataset to GCS'
17:14:45.387 | INFO    | Flow run 'rousing-sawfly' - Fetching URL Datasets from .yml
17:14:45.401 | INFO    | Flow run 'rousing-sawfly' - Created task run 'fetch_csv_from-0' for task 'fetch_csv_from'
17:14:45.401 | INFO    | Flow run 'rousing-sawfly' - Executing 'fetch_csv_from-0' immediately...
17:14:45.419 | INFO    | Task run 'fetch_csv_from-0' - Now fetching: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-04.csv.gz
17:14:46.267 | INFO    | Task run 'fetch_csv_from-0' - Finished in state Completed()
17:14:46.276 | INFO    | Flow run 'rousing-sawfly' - Created task run 'save_to_fs_with-0' for task 'save_to_fs_with'
17:14:46.277 | INFO    | Flow run 'rousing-sawfly' - Executing 'save_to_fs_with-0' immediately...


17:14:47.248 | INFO    | Task run 'save_to_fs_with-0' - Dataset 'green_tripdata_2019-04.csv.gz' contains: 514392 lines


17:14:47.256 | INFO    | Task run 'save_to_fs_with-0' - Finished in state Completed()
17:14:47.271 | INFO    | Flow run 'rousing-sawfly' - Created task run 'load_into_gcs_with-0' for task 'load_into_gcs_with'
17:14:47.271 | INFO    | Flow run 'rousing-sawfly' - Executing 'load_into_gcs_with-0' immediately...
17:14:47.363 | INFO    | Task run 'load_into_gcs_with-0' - Getting bucket 'iobruno_dtc_datalake_raw'.
17:14:47.918 | INFO    | Task run 'load_into_gcs_with-0' - Uploading from PosixPath('/Users/iobruno/Vault/data-engineering-zoomcamp/week2/prefect/datasets/green_tripdata_2019-04.parquet.gz') to the bucket 'iobruno_dtc_datalake_raw' path 'green/green_tripdata_2019-04.parquet.gz'.
```



## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- [ ] 5
- [ ] 6
- [x] 8
- [ ] 10



## Submitting the solutions

* Form for submitting: https://forms.gle/PY8mBEGXJ1RvmTM97
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 8 February (Wednesday), 22:00 CET


## Solution

We will publish the solution here