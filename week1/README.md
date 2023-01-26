# Terraform Setup for GCP

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

