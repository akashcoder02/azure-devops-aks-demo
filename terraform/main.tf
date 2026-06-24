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
