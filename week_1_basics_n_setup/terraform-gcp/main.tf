terraform {
  required_version = "~> 1.0"

  # Ref.: https://cloud.google.com/docs/terraform/resource-management/store-state
  backend "gcs" {
    bucket = "iobruno-gcp-labs-tfstate"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.7.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.data_region
}

# Ref.: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "stg_nyc_dataset" {
  dataset_id = var.bqds_stg_nyc
  location   = var.data_region
}

# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "iobruno_lakehouse_raw" {
  name     = var.lakehouse_raw_bucket
  location = var.data_region

  # Cascade delete all objects within when the bucket is deleted
  force_destroy               = true
  uniform_bucket_level_access = true
  storage_class               = var.lakehouse_storage_class

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = var.lakehouse_blob_expiration
    }
    action {
      type = "Delete"
    }
  }
}
