resource "kubernetes_manifest" "tic_tac_toe_destinationrule" {

  manifest = {
    apiVersion = "networking.istio.io/v1"
    kind       = "DestinationRule"

    metadata = {
      name      = "tic-tac-toe"
      namespace = "default"
    }

    spec = {

      host = "tic-tac-toe"

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
    kubernetes_manifest.tic_tac_toe_virtualservice
  ]
}
