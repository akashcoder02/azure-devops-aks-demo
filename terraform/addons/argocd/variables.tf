variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "Existing AKS Resource Group"
  type        = string

  default = "rg-devops-demo"
}

variable "aks_name" {
  description = "Existing AKS Cluster Name"
  type        = string

  default = "aks-devops-demo"
}

variable "argocd_namespace" {
  description = "Namespace where Argo CD will be installed"
  type        = string

  default = "argocd"
}

variable "argocd_release_name" {
  description = "Helm Release Name"
  type        = string

  default = "argocd"
}

variable "argocd_chart_version" {
  description = "Argo CD Helm Chart Version"
  type        = string

  default = "8.3.0"
}

variable "create_namespace" {
  description = "Create Argo CD namespace"
  type        = bool

  default = true
}