# ==========================================================
# SECURITY OUTPUTS
# ==========================================================

output "peer_authentication_name" {

  description = "PeerAuthentication Resource"

  value = kubectl_manifest.peer_authentication.name

}

output "authorization_policy_name" {

  description = "AuthorizationPolicy Resource"

  value = kubectl_manifest.authorization_policy.name

}

output "request_authentication_name" {

  description = "RequestAuthentication Resource"

  value = kubectl_manifest.request_authentication.name

}
