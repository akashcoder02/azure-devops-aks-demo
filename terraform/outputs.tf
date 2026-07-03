output "resource_group_name" {
  value = module.rg.resource_group_name
}

output "acr_name" {
  value = module.acr.acr_name
}

output "aks_name" {
  value = module.aks.aks_name
}

output "acr_login_server" {
  value = "${module.acr.acr_name}.azurecr.io"
}

output "keyvault_name" {
  value = module.keyvault.keyvault_name
}

output "keyvault_id" {
  value = module.keyvault.keyvault_id
}

output "keyvault_uri" {
  value = module.keyvault.keyvault_uri
}