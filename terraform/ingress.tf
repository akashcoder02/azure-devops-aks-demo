resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true

  values = [
    var.environment == "production" ? <<EOF
controller:
  service:
    type: LoadBalancer
    externalTrafficPolicy: Local

    # annotations removed

  ingressClassResource:
    default: true
EOF
    : <<EOF
controller:
  service:
    type: ClusterIP

  ingressClassResource:
    default: true
EOF
  ]
}