resource "kubernetes_manifest" "virtualservice" {

  for_each = var.applications

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "VirtualService"

    metadata = {
      name      = each.key
      namespace = var.namespace
    }

    spec = {

      gateways = [
        kubernetes_manifest.gateway.manifest.metadata.name
      ]

      hosts = [
        var.host
      ]

      http = [
        {
          match = [
            {
              uri = {
                regex = "^/${each.key}(/|$)(.*)"
              }
            }
          ]

          rewrite = {
            uriRegexRewrite = {
              match   = "^/${each.key}(/|$)(.*)"
              rewrite = "/$2"
            }
          }

          retries = {
            attempts      = 3
            perTryTimeout = "2s"
            retryOn       = "gateway-error,connect-failure,refused-stream,5xx"
          }

          timeout = "5s"

          route = [
            {
              destination = {
                host = each.key
                port = {
                  number = var.service_port
                }
              }
              weight = 100
            }
          ]
        }
      ]
    }
  }

  depends_on = [
    kubernetes_manifest.gateway
  ]
}