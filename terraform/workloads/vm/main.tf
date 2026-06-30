####################################################
# Network Module
####################################################

module "network" {

  source = "../../modules/network"

  resource_group_name = var.resource_group_name
  location            = var.location

  vnet_name   = var.vnet_name
  subnet_name = var.subnet_name

  address_space   = var.address_space
  subnet_prefixes = var.subnet_prefixes

}

####################################################
# Virtual Machine Module
####################################################

module "vm" {

  source = "../../modules/vm"

  count = var.vm_count

  resource_group_name = var.resource_group_name

  location = var.location

  subnet_id = module.network.subnet_id

  vm_name = format("%s-%02d", var.vm_name, count.index + 1)

  vm_size = var.vm_size

  admin_username = var.admin_username

  public_key = var.public_key

  os_disk_size_gb = var.os_disk_size_gb

  public_ip_enabled = var.public_ip_enabled

}