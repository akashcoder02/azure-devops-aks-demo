# ==========================================================
# SECURITY OUTPUTS
# ==========================================================

output "peer_authentication_names" {

  description = "PeerAuthentication Resources"

  value = [
    for resource in kubectl_manifest.peer_authentication :
    resource.name
  ]

}

output "authorization_policy_names" {

  description = "AuthorizationPolicy Resources"

  value = [
    for resource in kubectl_manifest.authorization_policy :
    resource.name
  ]

}

output "request_authentication_names" {

  description = "RequestAuthentication Resources"

  value = [
    for resource in kubectl_manifest.request_authentication :
    resource.name
  ]

}