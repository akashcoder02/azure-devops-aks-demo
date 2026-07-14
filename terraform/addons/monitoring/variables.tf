variable "namespace" {
  description = "Namespace where monitoring components will be installed"
  type        = string
  default     = "monitoring"
}

variable "helm_chart_version" {
  description = "Version of the kube-prometheus-stack Helm chart"
  type        = string
  default     = "75.10.0"
}

variable "create_namespace" {
  description = "Create monitoring namespace"
  type        = bool
  default     = true
}

variable "key_vault_name" {
  description = "Azure Key Vault name"
  type        = string
  default     = "agdevopskv2026"
}

variable "key_vault_resource_group" {
  description = "Resource Group containing the Key Vault"
  type        = string
  default     = "rg-devops-demo"
}

variable "grafana_admin_secret_name" {
  description = "Key Vault secret containing Grafana admin password"
  type        = string
  default     = "grafana-admin-password"
}

variable "grafana_service_type" {
  description = "Grafana Service Type"
  type        = string
  default     = "ClusterIP"
}

variable "prometheus_service_type" {
  description = "Prometheus Service Type"
  type        = string
  default     = "ClusterIP"
}

variable "grafana_storage_size" {
  description = "Grafana PVC Size"
  type        = string
  default     = "10Gi"
}

variable "prometheus_storage_size" {
  description = "Prometheus PVC Size"
  type        = string
  default     = "20Gi"
}

variable "alertmanager_storage_size" {
  description = "Alertmanager PVC Size"
  type        = string
  default     = "5Gi"
}