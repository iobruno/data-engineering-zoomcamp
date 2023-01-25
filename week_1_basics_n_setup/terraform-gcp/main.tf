terraform {
  required_version = "~> 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.50.0"
    }
  }
}

provider "google" {
  project = "iobruno-data-eng-zoomcamp"
  region  = "us-central1-a"
}

# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "dtc_datalake_raw" {
  name     = "iobruno_dtc_datalake_raw"
  location = "us-central1"

  # Cascade delete all objects within when the bucket is deleted
  force_destroy               = true
  uniform_bucket_level_access = true
  storage_class               = "STANDARD"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      # Age is defined in number of days
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Ref.: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dtc_datawarehouse_raw" {
  dataset_id = "dtc_datawarehouse_raw"
  location   = "us-central1"
}
