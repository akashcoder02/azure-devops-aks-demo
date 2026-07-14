data "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-devops-demo"
  resource_group_name = "rg-devops-demo"
}
