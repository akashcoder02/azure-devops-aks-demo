resource "kubernetes_namespace" "argocd" {

  count = var.create_namespace ? 1 : 0

  metadata {
    name = var.argocd_namespace

    labels = {
      app         = "argocd"
      managed-by  = "terraform"
      environment = "platform"
    }
  }
}