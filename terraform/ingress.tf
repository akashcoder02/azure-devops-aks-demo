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
    externalTrafficPolicy: Cluster

    annotations:
      service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: /healthz

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