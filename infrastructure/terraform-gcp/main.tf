resource "google_bigquery_dataset" "this" {
  dataset_id = var.raw_nyc_tlc_record_dataset
  location   = var.data_region
}

module "gcs" {
  source = "./cloud-storage"

  name    = var.lakehouse_raw_bucket
  region  = var.data_region
}
