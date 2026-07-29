resource "kubernetes_namespace" "istio_system" {

  count = var.create_namespace ? 1 : 0

  metadata {

    name = var.istio_namespace

    labels = {
      app         = "istio"
      managed-by  = "terraform"
      environment = "platform"
    }

  }

}