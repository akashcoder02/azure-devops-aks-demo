variable "subscription_id" {}

variable "resource_group_name" {
  default = "rg-devops-demo"
}

variable "location" {
  default = "Central India"
}

variable "acr_name" {
  default = "agdevopsacr2026"
}

variable "aks_name" {
  default = "aks-devops-demo"
}
variable "keyvault_name" {
  default = "agdevopskv2026"
}

variable "github_sp_object_id" {
  description = "GitHub Actions Service Principal Object ID"
  type        = string
}

variable "environment" {
  description = "Deployment environment"

  type = string

  validation {
    condition     = contains(["development", "production"], var.environment)
    error_message = "Environment must be either development or production."
  }
}