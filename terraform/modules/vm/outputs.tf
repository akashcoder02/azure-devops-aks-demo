output "vm_id" {
  description = "Virtual Machine ID"
  value       = azurerm_linux_virtual_machine.this.id
}

output "vm_name" {
  description = "Virtual Machine Name"
  value       = azurerm_linux_virtual_machine.this.name
}

output "vm_size" {
  description = "Virtual Machine Size"
  value       = azurerm_linux_virtual_machine.this.size
}

output "admin_username" {
  description = "VM Admin Username"
  value       = azurerm_linux_virtual_machine.this.admin_username
}

output "network_interface_id" {
  description = "Network Interface ID"
  value       = azurerm_network_interface.this.id
}

output "network_security_group_id" {
  description = "Network Security Group ID"
  value       = azurerm_network_security_group.this.id
}

output "private_ip" {
  description = "Private IP Address"
  value       = azurerm_network_interface.this.private_ip_address
}

output "public_ip" {
  description = "Public IP Address"
  value       = var.public_ip_enabled ? azurerm_public_ip.this[0].ip_address : null
}

output "public_ip_id" {
  description = "Public IP Resource ID"
  value       = var.public_ip_enabled ? azurerm_public_ip.this[0].id : null
}