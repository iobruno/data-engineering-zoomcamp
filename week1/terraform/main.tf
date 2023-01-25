terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.50.0"
    }
  }
}

provider "google" {
    project = "iobruno-data-eng-zoomcamp"
    region = "us-central1-a"
}