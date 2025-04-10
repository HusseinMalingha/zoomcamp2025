terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.29.0"
    }
  }
}

provider "google" {
  project     = "awesome-ripsaw-373013"
  region      = "asia-south1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "awesome-ripsaw-373013-terra-bucket"
  location      = "asia-south1"
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