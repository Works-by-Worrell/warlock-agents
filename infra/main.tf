terraform {
  required_version = ">= 1.5.0"
  backend "gcs" {
    bucket = "worksbyworrell-tf-state"
    prefix = "warlock-agents/prod"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# TODO: Define core resource blocks for Cloud Run, Firestore, Secret Manager, PubSub, and Scheduler
# (Refer to 0001-cloud-migration-blueprint.md Phase 2 for details)
