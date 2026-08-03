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

    canary_enabled = optional(bool, false)

    primary = optional(object({
      version = string
      weight  = number
      }), {
      version = "v1"
      weight  = 100
    })

    canary = optional(object({
      version = string
      weight  = number
      }), {
      version = "v2"
      weight  = 0
    })
  }))

  validation {
    condition = alltrue([
      for app in values(var.applications) :
      app.primary.weight + app.canary.weight == 100
    ])

    error_message = "For each application, primary.weight and canary.weight must equal 100."
  }
}

# ==========================================================
# TRAFFIC MANAGEMENT OVERRIDES
# ==========================================================

variable "traffic_application" {
  description = "Application to override traffic configuration"
  type        = string
  default     = ""
}

variable "primary_weight_override" {
  description = "Override primary traffic weight"
  type        = number
  default     = -1

  validation {
    condition     = var.primary_weight_override == -1 || (var.primary_weight_override >= 0 && var.primary_weight_override <= 100)
    error_message = "Primary traffic override must be between 0 and 100 or -1."
  }
}

variable "canary_weight_override" {
  description = "Override canary traffic weight"
  type        = number
  default     = -1

  validation {
    condition     = var.canary_weight_override == -1 || (var.canary_weight_override >= 0 && var.canary_weight_override <= 100)
    error_message = "Canary traffic override must be between 0 and 100 or -1."
  }
}

variable "canary_enabled_override" {
  description = "Override canary enabled flag"
  type        = bool