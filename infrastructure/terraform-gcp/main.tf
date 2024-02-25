resource "google_bigquery_dataset" "this" {
  dataset_id = var.raw_nyc_tlc_record_dataset
  location   = var.data_region
}

resource "google_storage_bucket" "this" {
  name      = var.lakehouse_raw_bucket
  location  = var.data_region

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
