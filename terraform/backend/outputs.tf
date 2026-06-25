output "resource_group_name" {
  value = azurerm_resource_group.backend.name
}

output "storage_account_name" {
  value = azurerm_storage_account.backend.name
}

output "container_name" {
  value = azurerm_storage_container.backend.name
}
