variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "gcp_region" {
  description = "Region for GCP Resources. Ref.: https://cloud.google.com/about/locations"
  type        = string
  default     = "us-central1"
}

variable "bq_stg_nyc_dataset" {
  description = "BigQuery Dataset name for the Staging area of the Warehouse"
  type        = string
}

variable "gcs_datalake_raw_bucket" {
  description = "Bucket name for storing data in Raw Layer of the Datalake"
  type        = string
}

variable "gcs_storage_class" {
  description = "Google Cloud Storage Storage Class"
  type        = string
  default     = "STANDARD"
}

variable "gcs_blob_lifecycle_expiration_in_days" {
  description = "Number of days in the object lifecycle before expiration"
  type        = number
  default     = 30
}
