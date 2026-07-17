variable "project_id" {
  type        = string
  description = "The target GCP project ID."
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Target regional compute zone optimized for cost and features."
}

variable "domain_name" {
  type        = string
  default     = "warlock.worksbyworrell.com"
  description = "Custom ingress route for the portfolio entrypoint."
}
