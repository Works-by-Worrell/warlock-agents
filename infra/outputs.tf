output "cloud_run_url" {
  value       = google_cloud_run_v2_service.warlock_agents.uri
  description = "The dynamic, system-assigned public URL for the Cloud Run instance."
}
