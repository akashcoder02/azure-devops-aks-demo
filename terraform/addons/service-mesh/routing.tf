resource "kubernetes_manifest" "tic_tac_toe_virtualservice" {

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "VirtualService"

    metadata = {
      name      = "tic-tac-toe"
      namespace = "default"
    }

    spec = {

      gateways = [
        kubernetes_manifest.tic_tac_toe_gateway.manifest.metadata.name
      ]

      hosts = [
        "*"
      ]

      http = [
        {
          match = [
            {
              uri = {
                prefix = "/"
              }
            }
          ]

          route = [
            {
              destination = {
                host = "tic-tac-toe"

                port = {
                  number = 80
                }
              }
            }
          ]
        }
      ]
    }
  }

  depends_on = [
    kubernetes_manifest.tic_tac_toe_gateway
  ]
}
