# Terraform Setup for GCP

## Initial Setup

Download and install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk) for your platform, following the instructions on the page

On the GCP Console in the web, create a new `Service Account` with the roles below, and export the key with JSON format:
    - `BigQuery Admin`
    - `Storage Admin`
    - `Storage Object Admin`

Export an environment variables named `GOOGLE_APPLICATION_CREDENTIALS` pointing to the full path where the .json credentials file is located:

```shell
export GOOGLE_APPLICATION_CREDENTIALS=/some/path/to/gcp-credentials.json
```

Execute the command below to ensure applications will now use the privileges you've set up on the Service Account

```shell
gcloud auth application-default login
```

**Enable BigQuery API on your GCP Project:**

Visit the [BigQuery API Console](https://console.developers.google.com/apis/api/bigquery.googleapis.com/overview) and enable it

![gcp-bigquery-api](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week1_gcp_bigquery_api.png)


## Up & Running with Terraform

**1.**: Create the GCS Bucket to serve as the backend for Terraform

In Google Cloud Storage, create a bucket that Terraform will use as its backend to save state:

![tfstate-gcp-bucket](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/assets/week1_tfstate_gcp_bucket.png)


**2.** Configure Terraform backend for GCS:

- In `main.tf`, under the `backend "gcs"`, edit the `bucket` name to use the one defined in step 1

- Initialize Terraform backend with:
```shell
terraform init
```

**3.** Terraform Plan & Apply

```shell
terraform plan
```

```shell
terraform apply
```

## Terraform Best Practises

Following the best practises for Terraform,

The variables that might contain sensitive information were set on `terraform.tfvars` (which, **for educational purposes only**, is set to *not* be ignored in version control - **do NOT use this for real-world scenarios**)

- GCP Project ID
- Bucket name for the RAW Datalake data
- BigQuery Dataset name for the Staging Data

## TODO:
- [x] Configure Google Cloud Storage as the backend for Terraform States
- [x] Extract sensitive data from variables.tf into *.tfvars
- [ ] Consider using Terraform modules as the project expands further