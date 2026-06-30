variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
}

variable "location" {
  description = "Azure Region"
  type        = string
}

variable "vnet_name" {
  description = "Virtual Network Name"
  type        = string
}

variable "subnet_name" {
  description = "Subnet Name"
  type        = string
}

variable "address_space" {
  description = "VNet Address Space"
  type        = list(string)
}

variable "subnet_prefixes" {
  description = "Subnet Prefixes"
  type        = list(string)
}
