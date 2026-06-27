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

  depends_on = [
    module.aks,
    module.acr
  ]
}
