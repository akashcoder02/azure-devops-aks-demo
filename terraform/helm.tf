locals {
  ingress_service_types = {
    development = "ClusterIP"
    production  = "LoadBalancer"
  }

  ingress_service_type = local.ingress_service_types[var.environment]
}

provider "helm" {
  kubernetes = {
    host                   = module.aks.host
    client_certificate     = base64decode(module.aks.client_certificate)
    client_key             = base64decode(module.aks.client_key)
    cluster_ca_certificate = base64decode(module.aks.cluster_ca_certificate)
  }
}

