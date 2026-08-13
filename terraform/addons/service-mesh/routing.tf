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

        merge(

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
              attempts      = var.retry_attempts
              perTryTimeout = var.per_try_timeout
              retryOn       = "gateway-error,connect-failure,refused-stream,5xx"
            }

            timeout = var.request_timeout

            route = [

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
                ) ? var.primary_weight_override : each.value.primary.weight
              },

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
                ) ? var.canary_weight_override : each.value.canary.weight
              }

            ]
          },

          (
            var.fault_delay_enabled || var.fault_abort_enabled
            ) ? {

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

          } : {}

        )

      ]

    }

  })

  depends_on = [
    kubectl_manifest.gateway
  ]
}