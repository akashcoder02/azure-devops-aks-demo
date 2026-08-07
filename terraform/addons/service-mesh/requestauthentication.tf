# ==========================================================
# REQUEST AUTHENTICATION (JWT)
# ==========================================================

resource "kubectl_manifest" "request_authentication" {

  for_each = (
    var.jwt_enabled &&
    trimspace(var.jwt_issuer) != "" &&
    trimspace(var.jwt_jwks_uri) != ""
  ) ? var.applications : {}

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

          issuer = var.jwt_issuer

          jwksUri = var.jwt_jwks_uri

        }

      ]

    }

  })

  depends_on = [

    kubectl_manifest.authorization_policy

  ]

}