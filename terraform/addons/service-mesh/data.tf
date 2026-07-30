data "azurerm_kubernetes_cluster" "aks" {

  name = var.aks_name

  resource_group_name = var.resource_group_name

}

data "kubernetes_service" "istio_ingressgateway" {

  metadata {
    name      = "istio-ingressgateway"
    namespace = var.istio_namespace
  }

  depends_on = [
    helm_release.istio_ingressgateway
  ]
}
