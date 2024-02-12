variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "data_region" {
  description = "Region for GCP Resources. Ref.: https://cloud.google.com/about/locations"
  type        = string
  default     = "us-central1"
}

variable "bigquery_raw_nyc_tlc" {
  description = "BigQuery Dataset for the raw data from NYC trip record data"
  type        = string
}

variable "lakehouse_raw_bucket" {
  description = "Bucket name for storing data in Raw Layer of the Datalake"
  type        = string
}

variable "lakehouse_storage_class" {
  description = "Google Cloud Storage Storage Class"
  type        = string
  default     = "STANDARD"
}

variable "lakehouse_blob_expiration" {
  description = "Number of days in the object lifecycle before expiration"
  type        = number
  default     = 30
}
