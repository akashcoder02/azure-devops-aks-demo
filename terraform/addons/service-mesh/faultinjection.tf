# ==========================================================
# FAULT INJECTION
# ==========================================================

resource "kubectl_manifest" "fault_injection" {
  for_each = {
    for name, app in var.applications :
    name => app
    if var.fault_delay_enabled || var.fault_abort_enabled
  }

  yaml_body = yamlencode({
    apiVersion = "networking.istio.io/v1"
    kind       = "VirtualService"

    metadata = {
      name      = "${each.key}-fault"
      namespace = var.namespace

      labels = {
        application = each.key
        managed-by  = "terraform"
        module      = "service-mesh-resilience"
      }
    }

    spec = {
      hosts = [
        var.host
      ]

      gateways = [
        var.gateway_name
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
              rewrite = "/\\2"
            }
          }

          fault = merge(
            var.fault_delay_enabled ? {
              delay = {
                percentage = {
                  value = var.fault_delay_percentage
                }

                fixedDelay = var.fault_delay
              }
            } : {},

            var.fault_abort_enabled ? {
              abort = {
                percentage = {
                  value = var.fault_abort_percentage
                }

                httpStatus = var.fault_abort_status
              }
            } : {}
          )

          route = [
            {
              destination = {
                host = each.key

                port = {
                  number = each.value.service_port
                }
              }
            }
          ]
        }
      ]
    }
  })

  depends_on = [
    kubectl_manifest.gateway,
    kubectl_manifest.virtualservice
  ]
}