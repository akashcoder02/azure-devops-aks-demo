output "argocd_release_name" {
  description = "Argo CD Helm Release Name"

  value = helm_release.argocd.name
}

output "argocd_namespace" {
  description = "Namespace where Argo CD is installed"

  value = helm_release.argocd.namespace
}

output "argocd_chart" {
  description = "Argo CD Helm Chart"

  value = helm_release.argocd.chart
}

output "argocd_chart_version" {
  description = "Installed Argo CD Chart Version"

  value = helm_release.argocd.version
}

output "argocd_status" {
  description = "Helm Release Status"

  value = helm_release.argocd.status
}