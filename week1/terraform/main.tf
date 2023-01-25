terraform {
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
resource "google_storage_bucket" "gcs_datalake_raw_bucket" {
  name     = "iobruno_dtc_datalake_raw"
  location = "us-central1"

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  # Cascade delete all objects within when the bucket is deleted
  force_destroy = true
}
