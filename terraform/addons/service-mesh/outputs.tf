output "istio_namespace" {
  description = "Istio Namespace"

  value = var.istio_namespace
}

output "istio_status" {
  description = "Istio Control Plane Status"

  value = helm_release.istiod.status
}

output "istio_version" {
  description = "Installed Istio Version"

  value = helm_release.istiod.version
}

output "gateway_status" {
  description = "Ingress Gateway Status"

  value = helm_release.istio_ingressgateway.status
}

output "gateway_version" {
  description = "Ingress Gateway Version"

  value = helm_release.istio_ingressgateway.version
}