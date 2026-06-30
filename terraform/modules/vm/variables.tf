
variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
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

variable "allowed_inbound_ports" {
  type = list(number)

  default = [
    22
  ]
}

variable "nsg_name" {
  type = string

  default = ""
}

variable "subnet_id" {
  type = string
}