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

output "istio_ingress_ip" {
  description = "Istio Ingress Gateway External IP"

  value = try(
    data.kubernetes_service.istio_ingressgateway.status[0].load_balancer[0].ingress[0].ip,
    null
  )
}

output "gateway_name" {
  value = var.gateway_name
}

output "virtualservice_names" {
  description = "Virtual Service Names"

  value = keys(var.applications)
}

output "destinationrule_names" {
  description = "Destination Rule Names"

  value = keys(var.applications)
}

output "application_urls" {
  description = "Application URLs via Istio"

  value = try(
    {
      for app in keys(var.applications) :
      app => "http://${data.kubernetes_service.istio_ingressgateway.status[0].load_balancer[0].ingress[0].ip}/${app}"
    },
    {}
  )
}