resource "kubernetes_manifest" "gateway" {

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "Gateway"

    metadata = {
      name      = "platform-gateway"
      namespace = var.namespace
    }

    spec = {
      selector = {
        istio = "ingressgateway"
      }

      servers = [
        {
          port = {
            number   = 80
            name     = "http"
            protocol = "HTTP"
          }

          hosts = [
            var.host
          ]
        }
      ]
    }
  }

  depends_on = [
    helm_release.istio_ingressgateway
  ]
}