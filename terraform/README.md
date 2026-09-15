# Terraform Foundation

[Project guide](../docs/README.md) · [Add-ons](addons/README.md)

## Root composition

[main.tf](main.tf) invokes resource-group, ACR, AKS, and Key Vault modules and creates role assignments.

| Component | Configuration |
|---|---|
| Resource group | Default rg-devops-demo |
| Region | Default Central India |
| AKS | Default aks-devops-demo; one Standard_B2s node |
| ACR | Default agdevopsacr2026; see modules/acr |
| Key Vault | Default agdevopskv2026; Azure RBAC authorization |
| AKS identity | System-assigned; separate kubelet and secrets-provider identities exposed |
| Secrets provider | Key Vault CSI add-on with rotation enabled |
| NGINX ingress | Helm release managed by ingress.tf |

Role assignments grant the AKS kubelet AcrPull, the secrets-provider identity Key Vault Secrets User, and the configured GitHub principal/current provisioning identity Key Vault Secrets Officer.

The [network module](modules/network/main.tf) defines a VNet and subnet but is not called by main.tf. Do not interpret its presence as a custom VNet attached to AKS.

## State bootstrap

[backend/main.tf](backend/main.tf) defines the resource group, Storage Account, and private blob container used for Terraform state. The main root expects that backend to exist before initialization.

[providers.tf](providers.tf) configures:

| Backend field | Value in source |
|---|---|
| Resource group | rg-tf-backend |
| Storage account | agtfstate2026xyz |
| Container | tfstate |
| State key | terraform.tfstate |

The bootstrap root has no remote backend declaration in its inspected provider configuration. Plan where bootstrap state is retained; creating the storage resources does not automatically migrate bootstrap state into them.

## Environment behavior

The required environment variable accepts development or production. ingress.tf selects ClusterIP for development and LoadBalancer for production.

The selection does not create separate state keys, namespaces, or AKS clusters. Existing resource-name defaults remain shared. Treat the setting as exposure configuration, not environment isolation.

## Providers and access

AzureRM is constrained to the 4.x family. The Helm provider connects using certificate material from the AKS module. Add-on roots define their own provider requirements and connections. Committed lock files record provider selections.

terraform.tfvars includes subscription/principal identifiers. These are identifiers rather than credential values, but they tie the configuration to the original environment. Workflows supply Azure authentication separately.

## Lifecycle entry points

The [infra workflow](../.github/workflows/infra.yaml) authenticates to Azure, optionally recovers a deleted vault, initializes and validates Terraform, plans and applies the root, waits for role propagation, and creates a demonstration Key Vault secret.

The [destroy workflow](../.github/workflows/destroy.yaml) destroys the core root. Local start.sh and stop.sh also perform lifecycle operations. Starting is provisioning; stopping is destruction, not pause/resume.

Review state, environment, dependencies, and resource names before using lifecycle automation. Platform add-ons depend on the cluster and should be considered when planning removal.

## Scope limitations

The default cluster is not sized or replicated to establish high availability. Key Vault purge protection is disabled in the inspected module. There is no environment-specific state design in this root. The workflows and local scripts are not interchangeable in all inputs; notably the root environment variable has no default.
