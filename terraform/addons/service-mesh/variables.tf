variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "Existing AKS Resource Group"
  type        = string
  default     = "rg-devops-demo"
}

variable "aks_name" {
  description = "Existing AKS Cluster Name"
  type        = string
  default     = "aks-devops-demo"
}

variable "istio_namespace" {
  description = "Namespace where Istio will be installed"
  type        = string
  default     = "istio-system"
}

variable "create_namespace" {
  description = "Create Istio namespace"
  type        = bool
  default     = true
}

variable "istio_version" {
  description = "Istio Helm Chart Version"
  type        = string
  default     = "1.27.1"
}

variable "gateway_version" {
  description = "Istio Gateway Chart Version"
  type        = string
  default     = "1.27.1"
}

variable "namespace" {
  description = "Kubernetes Namespace"
  type        = string
  default     = "default"
}

variable "host" {
  description = "Application Host"
  type        = string
  default     = "*"
}

variable "gateway_name" {
  description = "Istio Gateway Name"
  type        = string
  default     = "platform-gateway"
}

variable "applications" {
  description = "Applications to expose through Istio"

  type = map(object({
    service_port = number
  }))
}