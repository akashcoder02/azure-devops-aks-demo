variable "subscription_id" {}

variable "resource_group_name" {
  default = "rg-devops-IDP"
}

variable "location" {
  default = "Central India"
}

variable "acr_name" {
  default = "agdevopsacr2026"
}

variable "aks_name" {
  default = "aks-devops-IDP"
}
variable "keyvault_name" {
  default = "agdevopskv2026"
}