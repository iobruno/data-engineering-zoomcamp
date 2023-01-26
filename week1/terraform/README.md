# Terraform Setup for GCP

Find the answers to [Homework 1 Part B here](https://github.com/iobruno/data-engineering-zoomcamp/blob/master/week1/terraform/HOMEWORK.md)

## Initial Setup
- Download and install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk) for your platform, following the instructions on the page

- On the GCP Console in the web, create a new `Service Account` with the roles below, and export the key with JSON format:
    - `BigQuery Admin`
    - `Storage Admin` 
    - `Storage Object Admin`

- Export an environment variables named `GOOGLE_APPLICATION_CREDENTIALS` pointing to the full path where the .json credentials file is located:
    
```
$ export GOOGLE_APPLICATION_CREDENTIALS=/some/path/to/gcp-credentials.json
```

- Execute the command below to ensure applications will now use the privileges you've set up on the Service Account

```
$ gcloud auth application-default login
```

## Up & Running with Terraform


Following the best practises for Terraform, 

The variables that might contain sensitive information were set on `terraform.tfvars` (which, **for educational purposes only**, is set to *not* be ignored in version control - **do NOT use this for real-world scenarios**)

- GCP Project ID
- Bucket name for the RAW Datalake data
- BigQuery Dataset name for the Staging Data
    
```
$ terraform apply
```

## TODO:
- [X] Configure Google Cloud Storage as the backend for Terraform States
- [X] Extract sensitive data from variables.tf into *.tfvars
- [ ] Consider using Terraform modules as the project expands further
