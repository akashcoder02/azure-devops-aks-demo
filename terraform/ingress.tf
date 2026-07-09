resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true

  values = [<<EOF
controller:
  service:
    type: ${local.ingress_service_type}
    externalTrafficPolicy: Local
  ingressClassResource:
    default: true
EOF
  ]
}