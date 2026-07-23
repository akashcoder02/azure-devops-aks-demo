resource "azurerm_storage_account" "devsecops" {

  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
  location            = var.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  min_tls_version = "TLS1_2"

  allow_nested_items_to_be_public = false

  tags = local.tags

}

resource "azurerm_storage_container" "security_reports" {

  name                  = var.security_reports_container
  storage_account_id    = azurerm_storage_account.devsecops.id
  container_access_type = "private"

}

resource "azurerm_storage_container" "security_history" {

  name                  = var.security_history_container
  storage_account_id    = azurerm_storage_account.devsecops.id
  container_access_type = "private"

}

resource "azurerm_storage_container" "sbom" {

  name                  = var.sbom_container
  storage_account_id    = azurerm_storage_account.devsecops.id
  container_access_type = "private"

}