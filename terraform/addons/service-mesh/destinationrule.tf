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

      subsets = each.value.canary_enabled ? [
        {
          name = each.value.primary.version

          labels = {
            version = each.value.primary.version
          }
        },
        {
          name = each.value.canary.version

          labels = {
            version = each.value.canary.version
          }
        }
      ] : []

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
            maxRetries               = 3
            idleTimeout              = "30s"
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