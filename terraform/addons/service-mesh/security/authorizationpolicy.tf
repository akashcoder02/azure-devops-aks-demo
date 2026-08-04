# ==========================================================
# AUTHORIZATION POLICY
# ==========================================================

resource "kubectl_manifest" "authorization_policy" {

  for_each = var.authorization_enabled ? var.applications : {}

  yaml_body = yamlencode({

    apiVersion = "security.istio.io/v1"

    kind = "AuthorizationPolicy"

    metadata = {

      name = each.key

      namespace = var.namespace

      labels = merge(

        local.common_labels,

        {

          application = each.key

        }

      )

    }

    spec = {

      selector = {

        matchLabels = {

          app = each.key

        }

      }

      action = "ALLOW"

      rules = [

        {

          from = [

            {

              source = {

                namespaces = [

                  var.namespace

                ]

              }

            }

          ]

        }

      ]

    }

  })

  depends_on = [

    kubectl_manifest.peer_authentication

  ]

}