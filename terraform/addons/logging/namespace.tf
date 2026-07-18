resource "kubernetes_namespace" "logging" {
  count = var.create_namespace ? 1 : 0

  metadata {
    name = var.namespace

    labels = {
      app         = "logging"
      managed-by  = "terraform"
      environment = "production"
    }
  }
}