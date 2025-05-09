terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  #  credentials = 
  project = "dtc-de-course-457906"
  region  = "australia-southeast1-a"
}



resource "google_storage_bucket" "data-lake-bucket" {
  name     = "data-lake-bucket-dtc-de-course-457906"
  location = "AUSTRALIA-SOUTHEAST1"

  # Optional, but recommended settings:
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "homework1_dataset"
  project    = "dtc-de-course-457906"
  location   = "australia-southeast1"
}