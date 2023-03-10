terraform {
  required_version = "~> 1.0"

  # Ref.: https://cloud.google.com/docs/terraform/resource-management/store-state
  backend "gcs" {
    bucket = "iobruno-training-gcp-tfstate"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.50.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "dtc_datalake_raw" {
  name     = var.gcs_datalake_raw_bucket
  location = var.gcp_region

  # Cascade delete all objects within when the bucket is deleted
  force_destroy               = true
  uniform_bucket_level_access = true
  storage_class               = var.gcs_storage_class

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = var.gcs_blob_lifecycle_expiration_in_days
    }
    action {
      type = "Delete"
    }
  }
}

# Ref.: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dtc_dw_staging" {
  dataset_id = var.bq_staging_dataset
  location   = var.gcp_region
}
