variable "subscription_id" {}

variable "location" {
  default = "Central India"
}

variable "resource_group_name" {
  default = "rg-tf-backend"
}

variable "storage_account_name" {
  default = "agtfstate2026xyz"
}

variable "container_name" {
  default = "tfstate"
}
