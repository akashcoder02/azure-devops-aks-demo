variable "resource_group_name" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "location" {
  description = "Azure Region"
  type        = string
}

variable "storage_account_name" {
  description = "DevSecOps Storage Account Name"
  type        = string
}

variable "security_reports_container" {
  description = "Security Reports Container"
  type        = string
  default     = "security-reports"
}

variable "security_history_container" {
  description = "Security History Container"
  type        = string
  default     = "security-history"
}

variable "sbom_container" {
  description = "SBOM Container"
  type        = string
  default     = "sbom"
}