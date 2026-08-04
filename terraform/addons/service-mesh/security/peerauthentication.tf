# ==========================================================
# PEER AUTHENTICATION
# ==========================================================

resource "kubectl_manifest" "peer_authentication" {

  for_each = var.applications

  yaml_body = yamlencode({

    apiVersion = "security.istio.io/v1"

    kind = "PeerAuthentication"

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

      mtls = {

        mode = var.mtls_mode

      }

    }

  })

  depends_on = [

    helm_release.istiod

  ]

}