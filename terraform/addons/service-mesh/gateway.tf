resource "kubernetes_manifest" "tic_tac_toe_gateway" {

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "Gateway"

    metadata = {
      name      = "tic-tac-toe-gateway"
      namespace = "default"
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
            "*"
          ]
        }
      ]
    }
  }

  depends_on = [
    helm_release.istio_ingressgateway
  ]
}