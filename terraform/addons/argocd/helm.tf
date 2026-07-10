resource "helm_release" "argocd" {

  name = var.argocd_release_name

  repository = "https://argoproj.github.io/argo-helm"

  chart = "argo-cd"

  version = var.argocd_chart_version

  namespace = var.argocd_namespace

  create_namespace = false

  wait = true

  atomic = true

  cleanup_on_fail = true

  timeout = 600

  depends_on = [
    kubernetes_namespace.argocd
  ]

}