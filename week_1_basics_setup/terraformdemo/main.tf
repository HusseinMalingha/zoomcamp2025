terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.29.0"
    }
  }
}

provider "google" {
  credentials = var.credentials
  project = var.project
  region  = var.location
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_class_name
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
}