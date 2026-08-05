# ==========================================================
# FAULT INJECTION
# ==========================================================

resource "kubectl_manifest" "fault_injection" {

  for_each = var.applications

  yaml_body = yamlencode({

    apiVersion = "networking.istio.io/v1"

    kind = "VirtualService"

    metadata = {

      name      = "${each.key}-fault"

      namespace = var.namespace

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

          fault = {

            delay = {

              percentage = {
                value = 100
              }

              fixedDelay = "5s"

            }

            abort = {

              percentage = {
                value = 0
              }

              httpStatus = 500

            }

          }

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

}