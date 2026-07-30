resource "kubernetes_manifest" "destinationrule" {

  for_each = var.applications

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "DestinationRule"

    metadata = {
      name      = each.key
      namespace = var.namespace
    }

    spec = {

      host = each.key

      trafficPolicy = {

        loadBalancer = {
          simple = "LEAST_REQUEST"
        }

        connectionPool = {

          tcp = {
            maxConnections = 100
          }

          http = {
            http1MaxPendingRequests  = 50
            maxRequestsPerConnection = 20
          }
        }

        outlierDetection = {
          consecutive5xxErrors = 5
          interval             = "30s"
          baseEjectionTime     = "30s"
          maxEjectionPercent   = 50
        }
      }
    }
  }

  depends_on = [
    kubernetes_manifest.virtualservice
  ]
}