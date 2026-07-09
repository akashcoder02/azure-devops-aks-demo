module "rg" {
  source = "./modules/rg"

  resource_group_name = var.resource_group_name
  location            = var.location
}

module "acr" {
  source = "./modules/acr"

  acr_name            = var.acr_name
  resource_group_name = module.rg.resource_group_name
  location            = module.rg.location
}

module "aks" {
  source = "./modules/aks"

  aks_name            = var.aks_name
  resource_group_name = module.rg.resource_group_name
  location            = module.rg.location
}

resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = module.acr.acr_id
  role_definition_name = "AcrPull"
  principal_id         = module.aks.kubelet_object_id

  skip_service_principal_aad_check = true

  depends_on = [
    module.aks,
    module.acr
  ]
}

resource "azurerm_role_assignment" "github_keyvault_secrets_officer" {

  scope                = module.keyvault.keyvault_id
  role_definition_name = "Key Vault Secrets Officer"

  principal_id = var.github_sp_object_id

  depends_on = [
    module.keyvault
  ]
}

resource "azurerm_role_assignment" "aks_keyvault_secrets_user" {

  scope                = module.keyvault.keyvault_id
  role_definition_name = "Key Vault Secrets User"

  principal_id = module.aks.keyvault_secret_identity_object_id

  depends_on = [
    module.keyvault,
    module.aks
  ]
}

module "keyvault" {
  source = "./modules/keyvault"

  keyvault_name       = var.keyvault_name
  resource_group_name = module.rg.resource_group_name
  location            = module.rg.location

  tenant_id = data.azurerm_client_config.current.tenant_id
}

resource "azurerm_role_assignment" "admin_keyvault_secrets_officer" {

  scope                = module.keyvault.keyvault_id
  role_definition_name = "Key Vault Secrets Officer"

  principal_id = data.azurerm_client_config.current.object_id

  depends_on = [
    module.keyvault
  ]
}