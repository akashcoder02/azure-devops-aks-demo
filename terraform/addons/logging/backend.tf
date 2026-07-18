terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tf-backend"
    storage_account_name = "agtfstate2026xyz"
    container_name       = "tfstate"
    key                  = "logging.tfstate"
  }
}
