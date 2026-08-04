# ==========================================================
# REQUEST AUTHENTICATION (JWT)
# ==========================================================

resource "kubectl_manifest" "request_authentication" {

  for_each = var.authorization_enabled ? var.applications : {}
  yaml_body = yamlencode({

    apiVersion = "security.istio.io/v1"

    kind = "RequestAuthentication"

    metadata = {

      name = "${each.key}-jwt"

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

      jwtRules = [

        {

          issuer = "https://example.com"

          jwksUri = "https://example.com/.well-known/jwks.json"

        }

      ]

    }

  })

  depends_on = [

    kubectl_manifest.authorization_policy

  ]

}