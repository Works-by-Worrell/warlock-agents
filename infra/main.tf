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

data "google_project" "project" {}

locals {
    gcp_services = [
        "firestore.googleapis.com",
        "artifactregistry.googleapis.com",
        "run.googleapis.com",
        "secretmanager.googleapis.com",
        "pubsub.googleapis.com",
        "cloudscheduler.googleapis.com",
        "cloudbuild.googleapis.com"
    ]
}

resource "google_project_service" "apis" {
    for_each            = toset(local.gcp_services)
    project             = var.project_id
    service             = each.value
    disable_on_destroy  = false
}

resource "google_firestore_database" "database" {
    project         = var.project_id
    name            = "(default)"
    location_id     = var.region
    type            = "FIRESTORE_NATIVE"
    deletion_policy = "DELETE"

    depends_on = [google_project_service.apis]
}

resource "google_artifact_registry_repository" "repo" {
    location        = var.region
    repository_id   = "worksbyworrell-registry"
    description     = "Docker repository optimized for minimal image retention"
    format          = "DOCKER"

    depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service" "warlock_agents" {
    name = "warlock-agents-core"
    location = var.region
    ingress = "INGRESS_TRAFFIC_ALL"

    template {
        scaling {
            max_instance_count = 3
            min_instance_count = 0
        }

        containers {
            image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}/warlock-agents-core:latest"

            resources {
                limits = {
                    cpu     = "1"
                    memory  = "512Mi"
                }
                startup_cpu_boost = true
            }

            env {
                name    = "FASTMCP_TRANSPORT"
                value   = "streamable-http"
            }

            env {
                name    = "GH_TOKEN"
                value_source {
                    secret_key_ref {
                        secret  = google_secret_manager_secret.github_token.secret_id
                        version = "latest"
                    }
                }
            }
        }
    }

    depends_on = [
        google_project_service.apis,
        google_secret_manager_secret_iam_member.github_token_accessor
    ]
}

resource "google_secret_manager_secret" "github_token" {
    secret_id = "github-app-token"
    replication {
        auto {}
    }

    depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_iam_member" "github_token_accessor" {
    secret_id = google_secret_manager_secret.github_token.secret_id
    role      = "roles/secretmanager.secretAccessor"
    member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"

    depends_on = [google_project_service.apis]
}

resource "google_artifact_registry_repository_iam_member" "cleanup_policy_binding" {
    project     = var.project_id
    location    = google_artifact_registry_repository.repo.location
    repository  = google_artifact_registry_repository.repo.name
    role        = "roles/artifactregistry.repoAdmin"
    member      = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"

    depends_on = [google_project_service.apis]
}

resource "google_cloud_scheduler_job" "purge_old_images" {
    name                = "cleanup-registry-layers"
    description         = "Trigger automated cleanup of dangling or historical container tags"
    schedule            = "0 0 * * 1"
    time_zone           = "America/Denver"
    attempt_deadline    = "320s"

    pubsub_target {
        topic_name  = google_pubsub_topic.cleanup_topic.id
        data        = base64encode("{\"action\": \"KEEP_3_TAGS\"}")

    }
    
    depends_on = [google_project_service.apis]
}

resource "google_pubsub_topic" "cleanup_topic" {
    name    = "artifact-registry-cleanup"

    depends_on = [google_project_service.apis]
}
