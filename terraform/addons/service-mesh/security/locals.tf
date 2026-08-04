# ==========================================================
# SERVICE MESH SECURITY LOCALS
# ==========================================================

locals {

  common_labels = {

    managed-by = "terraform"

    module = "service-mesh-security"

    environment = "platform"

  }

}
