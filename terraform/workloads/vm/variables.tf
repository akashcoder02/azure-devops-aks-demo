variable "subscription_id" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "vnet_name" {
  type    = string
  default = "idp-vnet"
}

variable "subnet_name" {
  type    = string
  default = "idp-subnet"
}

variable "address_space" {
  type = list(string)

  default = [
    "10.10.0.0/16"
  ]
}

variable "subnet_prefixes" {
  type = list(string)

  default = [
    "10.10.1.0/24"
  ]
}

variable "vm_name" {
  type = string
}

variable "vm_size" {
  type    = string
  default = "Standard_B2s"
}

variable "admin_username" {
  type = string
}

variable "public_key" {
  type = string
}

variable "os_disk_size_gb" {
  type    = number
  default = 64
}

variable "public_ip_enabled" {
  type    = bool
  default = true
}

variable "vm_count" {
  type    = number
  default = 1
}