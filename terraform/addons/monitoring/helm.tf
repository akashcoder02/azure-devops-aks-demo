resource "helm_release" "kube_prometheus_stack" {
  name       = "kube-prometheus-stack"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = var.helm_chart_version

  namespace        = var.namespace
  create_namespace = false

  depends_on = [
    kubernetes_namespace.monitoring
  ]

  values = [
    yamlencode({

      grafana = {
        enabled = true

        service = {
          type = var.grafana_service_type
        }

        persistence = {
          enabled = true
          size    = var.grafana_storage_size
        }
      }

      prometheus = {
        prometheusSpec = {
          storageSpec = {
            volumeClaimTemplate = {
              spec = {
                accessModes = ["ReadWriteOnce"]

                resources = {
                  requests = {
                    storage = var.prometheus_storage_size
                  }
                }
              }
            }
          }
        }

        service = {
          type = var.prometheus_service_type
        }
      }

      alertmanager = {
        enabled = true

        alertmanagerSpec = {
          storage = {
            volumeClaimTemplate = {
              spec = {
                accessModes = ["ReadWriteOnce"]

                resources = {
                  requests = {
                    storage = var.alertmanager_storage_size
                  }
                }
              }
            }
          }
        }
      }

      kubeStateMetrics = {
        enabled = true
      }

      nodeExporter = {
        enabled = true
      }

    })
  ]
}