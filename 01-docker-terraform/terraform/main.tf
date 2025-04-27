terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json"
  project     = "dtc-de-course-457906"
  region      = "us-central1"
  zone        = "us-central1-c"
}

resource "google_storage_bucket" "demo-bucket" {
  name     = "dtc-de-course-457906-demo-bucket"
  location = "US"

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
