output "monitoring_namespace" {
  description = "Monitoring namespace"
  value       = var.namespace
}

output "helm_release_name" {
  description = "Monitoring Helm release"
  value       = helm_release.kube_prometheus_stack.name
}

output "helm_chart_version" {
  description = "Installed kube-prometheus-stack version"
  value       = helm_release.kube_prometheus_stack.version
}

output "monitoring_status" {
  description = "Monitoring installation status"
  value       = helm_release.kube_prometheus_stack.status
}
