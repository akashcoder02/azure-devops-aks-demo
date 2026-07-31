resource "kubectl_manifest" "gateway" {

  yaml_body = <<YAML
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: platform-gateway
  namespace: ${var.namespace}
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "${var.host}"
YAML

  depends_on = [
    helm_release.istio_ingressgateway
  ]
}