resource "kubectl_manifest" "virtualservice" {

  for_each = var.applications

  yaml_body = yamlencode({

    apiVersion = "networking.istio.io/v1"

    kind = "VirtualService"

    metadata = {
      name      = each.key
      namespace = var.namespace
    }

    spec = {

      gateways = [
        var.gateway_name
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
              rewrite = "/\\2"
            }
          }

          retries = {
            attempts      = 3
            perTryTimeout = "2s"
            retryOn       = "gateway-error,connect-failure,refused-stream,5xx"
          }

          timeout = "5s"

          route = concat(

            [
              {
                destination = {
                  host   = each.key
                  subset = each.value.primary.version

                  port = {
                    number = each.value.service_port
                  }
                }

                weight = (
                  each.key == var.traffic_application &&
                  var.primary_weight_override >= 0
                )
                ? var.primary_weight_override
                : (
                    each.value.canary_enabled
                    ? each.value.primary.weight
                    : 100
                  )
              }
            ],

            (
              (
                each.key == var.traffic_application
                ? var.canary_enabled_override
                : each.value.canary_enabled
              )
            ) ? [

              {
                destination = {
                  host   = each.key
                  subset = each.value.canary.version

                  port = {
                    number = each.value.service_port
                  }
                }

                weight = (
                  each.key == var.traffic_application &&
                  var.canary_weight_override >= 0
                )
                ? var.canary_weight_override
                : each.value.canary.weight
              }

            ] : []

          )

        }
      ]

    }
  })

  depends_on = [
    kubectl_manifest.gateway
  ]
}