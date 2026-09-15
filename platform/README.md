# Shared Platform Configuration

[Project guide](../docs/README.md)

[config/platform.env](config/platform.env) supplies shared identifiers used by application scripts and the newer dashboard.

| Key | Source value |
|---|---|
| RESOURCE_GROUP | rg-devops-demo |
| LOCATION | centralindia |
| ACR_NAME | agdevopsacr2026 |
| AKS_NAME | aks-devops-demo |
| NAMESPACE | default |

These are configuration identifiers, not authentication credentials.

## Library helpers

[lib/validate-platform.sh](lib/validate-platform.sh) defines validation for Azure login, Docker, kubectl, and Terraform availability. The other library files are empty placeholders in the inspected snapshot.

## Portability boundaries

This directory is not the sole source of configuration. Resource names also appear in Terraform defaults/tfvars, GitHub secrets and literal workflow steps, Python services, GitOps manifests, and scripts/lib/config.sh.

Changing platform.env alone will not retarget the whole platform. A deployment into another account requires reviewing all of those inputs and the backend/state boundary.

The default namespace is shared by the example applications. No tenant isolation is established by this configuration file.
