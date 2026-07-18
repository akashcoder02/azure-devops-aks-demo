variable "namespace" {
  description = "Logging namespace"
  type        = string
  default     = "logging"
}

variable "create_namespace" {
  description = "Create logging namespace"
  type        = bool
  default     = true
}

variable "loki_chart_version" {
  description = "Loki Helm chart version"
  type        = string
  default     = "6.55.0"
}

variable "fluent_bit_chart_version" {
  description = "Fluent Bit Helm chart version"
  type        = string
  default     = "0.53.0"
}