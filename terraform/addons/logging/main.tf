resource "helm_release" "loki" {

  name       = "loki"
  repository = "https://grafana.github.io/helm-charts"
  chart      = "loki"

  version = var.loki_chart_version

  namespace        = var.namespace
  create_namespace = false

  depends_on = [
    kubernetes_namespace.logging[0]
  ]

  values = [
    file("${path.module}/values/loki-values.yaml")
  ]
}

resource "helm_release" "fluent_bit" {

  name       = "fluent-bit"
  repository = "https://fluent.github.io/helm-charts"
  chart      = "fluent-bit"

  version = var.fluent_bit_chart_version

  namespace        = var.namespace
  create_namespace = false

  depends_on = [
    helm_release.loki
  ]

  values = [
    file("${path.module}/values/fluent-bit-values.yaml")
  ]
}