output "storage_account_name" {

  value = azurerm_storage_account.devsecops.name

}

output "storage_account_id" {

  value = azurerm_storage_account.devsecops.id

}

output "security_reports_container" {

  value = azurerm_storage_container.security_reports.name

}

output "security_history_container" {

  value = azurerm_storage_container.security_history.name

}

output "sbom_container" {

  value = azurerm_storage_container.sbom.name

}