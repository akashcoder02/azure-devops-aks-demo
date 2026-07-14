resource "kubernetes_namespace" "monitoring" {
  count = var.create_namespace ? 1 : 0

  metadata {
    name = var.namespace

    labels = {
      app         = "monitoring"
      managed-by  = "terraform"
      environment = "production"
    }
  }
}
