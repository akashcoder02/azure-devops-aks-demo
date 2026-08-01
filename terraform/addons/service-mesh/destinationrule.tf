resource "kubectl_manifest" "destinationrule" {

  for_each = var.applications

  yaml_body = yamlencode({

    apiVersion = "networking.istio.io/v1"

    kind = "DestinationRule"

    metadata = {
      name      = each.key
      namespace = var.namespace
    }

    spec = {

      host = each.key

      subsets = concat(
        [
          {
            name = each.value.primary.version

            labels = {
              version = each.value.primary.version
            }
          }
        ],
        (
          each.key == var.traffic_application
          ? var.canary_enabled_override
          : each.value.canary_enabled
        ) ? [
          {
            name = each.value.canary.version

            labels = {
              version = each.value.canary.version
            }
          }
        ] : []
      )

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

  })

  depends_on = [
    kubectl_manifest.virtualservice
  ]
}