resource "helm_release" "argocd" {

  name = var.argocd_release_name

  repository = "https://argoproj.github.io/argo-helm"

  chart = "argo-cd"

  version = var.argocd_chart_version

  namespace = var.argocd_namespace

  create_namespace = false

  wait = true

  atomic = true

  cleanup_on_fail = true

  timeout = 600

  values = [
    yamlencode({
      configs = {
        cm = {
          "accounts.backstage" = "login"
        }

        rbac = {
          "policy.csv" = <<-EOT
            p, role:backstage-readonly, applications, get, */*, allow
            p, role:backstage-readonly, projects, get, *, allow
            g, backstage, role:backstage-readonly
          EOT
        }

        secret = {
          extra = {
            "accounts.backstage.password" = var.argocd_backstage_password_hash
          }
        }
      }
    })
  ]

  depends_on = [
    kubernetes_namespace.argocd
  ]
}