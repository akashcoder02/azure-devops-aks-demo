##############################################
# Public IP
##############################################

resource "azurerm_public_ip" "this" {

  count = var.public_ip_enabled ? 1 : 0

  name                = "${var.vm_name}-pip"
  location            = var.location
  resource_group_name = var.resource_group_name

  allocation_method = "Static"
  sku               = "Standard"

  tags = {
    ManagedBy = "Azure-IDP"
    Module    = "vm"
  }
}

##############################################
# Network Security Group
##############################################

resource "azurerm_network_security_group" "this" {

  name                = "${var.vm_name}-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name

  tags = {
    ManagedBy = "Azure-IDP"
    Module    = "vm"
  }
}

##############################################
# Allow SSH
##############################################

resource "azurerm_network_security_rule" "ssh" {

  name = "Allow-SSH"

  priority = 100

  direction = "Inbound"

  access = "Allow"

  protocol = "Tcp"

  source_port_range = "*"

  destination_port_range = "22"

  source_address_prefix = "*"

  destination_address_prefix = "*"

  resource_group_name = var.resource_group_name

  network_security_group_name = azurerm_network_security_group.this.name
}

##############################################
# Network Interface
##############################################

resource "azurerm_network_interface" "this" {

  name = "${var.vm_name}-nic"

  location = var.location

  resource_group_name = var.resource_group_name

  ip_configuration {

    name = "internal"

    subnet_id = var.subnet_id

    private_ip_address_allocation = "Dynamic"

    public_ip_address_id = var.public_ip_enabled ? azurerm_public_ip.this[0].id : null

  }

  tags = {
    ManagedBy = "Azure-IDP"
    Module    = "vm"
  }
}

##############################################
# Associate NIC with NSG
##############################################

resource "azurerm_network_interface_security_group_association" "this" {

  network_interface_id = azurerm_network_interface.this.id

  network_security_group_id = azurerm_network_security_group.this.id

}

##############################################
# Linux Virtual Machine
##############################################

resource "azurerm_linux_virtual_machine" "this" {

  name          = var.vm_name
  computer_name = var.vm_name

  location            = var.location
  resource_group_name = var.resource_group_name

  size = var.vm_size

  admin_username = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.this.id
  ]

  disable_password_authentication = true

  admin_ssh_key {

    username = var.admin_username

    public_key = var.public_key

  }

  os_disk {

    name = "${var.vm_name}-osdisk"

    caching = "ReadWrite"

    storage_account_type = "StandardSSD_LRS"

    disk_size_gb = var.os_disk_size_gb

  }

  source_image_reference {

    publisher = "Canonical"

    offer = "ubuntu-24_04-lts"

    sku = "server"

    version = "latest"

  }

  boot_diagnostics {
  }

  tags = {

    ManagedBy = "Azure-IDP"

    Platform = "Internal Developer Platform"

    ResourceType = "VirtualMachine"

    Template = "GenericLinux"

  }

  depends_on = [
    azurerm_network_interface_security_group_association.this
  ]
}