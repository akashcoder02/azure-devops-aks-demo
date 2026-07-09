variable "keyvault_name" {
  description = "Azure Key Vault Name"
  type        = string
}

variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
}

variable "location" {
  description = "Azure Region"
  type        = string
}

variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}

variable "github_sp_object_id" {
  description = "GitHub Actions Service Principal Object ID"
  type        = string
}