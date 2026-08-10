resource "kubectl_manifest" "destinationrule" {
  for_each = var.applications

  yaml_body = yamlencode({
    apiVersion = "networking.istio.io/v1"
    kind       = "DestinationRule"

    metadata = {
      name      = each.key
      namespace = var.namespace
    }

    spec = {
      host = each.key

      subsets = [
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
      ]

      trafficPolicy = {
        loadBalancer = {
          simple = "LEAST_REQUEST"
        }

        connectionPool = {
          tcp = {
            maxConnections = var.max_connections
          }

          http = {
            http1MaxPendingRequests  = var.max_connections
            maxRequestsPerConnection = var.max_requests_per_connection
            maxRetries               = var.retry_attempts
            idleTimeout              = var.idle_timeout
          }
        }

        outlierDetection = {
          consecutive5xxErrors = var.consecutive_errors
          interval             = var.outlier_interval
          baseEjectionTime      = var.base_ejection_time
          maxEjectionPercent    = 50
        }
      }
    }
  })

  depends_on = [
    kubectl_manifest.virtualservice
  ]
}