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
