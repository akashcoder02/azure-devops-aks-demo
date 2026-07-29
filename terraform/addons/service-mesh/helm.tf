resource "helm_release" "istio_base" {

  name = "istio-base"

  repository = "https://istio-release.storage.googleapis.com/charts"

  chart = "base"

  version = var.istio_version

  namespace = var.istio_namespace

  create_namespace = false

  wait = true

  atomic = true

  cleanup_on_fail = true

  timeout = 600

  depends_on = [
    kubernetes_namespace.istio_system
  ]
}

resource "helm_release" "istiod" {

  name = "istiod"

  repository = "https://istio-release.storage.googleapis.com/charts"

  chart = "istiod"

  version = var.istio_version

  namespace = var.istio_namespace

  create_namespace = false

  wait = true

  atomic = true

  cleanup_on_fail = true

  timeout = 600

  values = [
    <<-EOF
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
EOF
  ]

  depends_on = [
    helm_release.istio_base
  ]
}

resource "helm_release" "istio_ingressgateway" {

  name = "istio-ingressgateway"

  repository = "https://istio-release.storage.googleapis.com/charts"

  chart = "gateway"

  version = var.gateway_version

  namespace = var.istio_namespace

  create_namespace = false

  wait = true

  atomic = true

  cleanup_on_fail = true

  timeout = 600

  depends_on = [
    helm_release.istiod
  ]

}