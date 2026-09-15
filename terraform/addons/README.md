# Platform Add-ons

[Project guide](../../docs/README.md) · [Terraform foundation](../README.md)

Each implemented add-on directory is a separate Terraform root, operated by dedicated GitHub workflows. They look up the existing AKS cluster rather than create a second cluster.

| Add-on | Components | Namespace/location | State |
|---|---|---|---|
| argocd | Argo CD Helm chart | argocd | argocd.tfstate |
| monitoring | kube-prometheus-stack | monitoring | monitoring.tfstate |
| logging | Loki and Fluent Bit | logging | logging.tfstate |
| service-mesh | Istio base, istiod, gateway, routing and policies | istio-system plus default app namespace | service-mesh.tfstate |
| devsecops | Storage Account and private report/history/SBOM containers | Azure resource group | backend.tf is empty |

The first four use the same configured Azure Storage backend with different keys. Separate folders do not themselves guarantee separate remote state: DevSecOps currently lacks that configuration.

## Argo CD

[argocd/helm.tf](argocd/helm.tf) installs the chart; the source pins chart version 8.3.0 through configuration. The installation workflow additionally creates a repository credential Secret. Application definitions are in [gitops/projects](../../gitops/projects), not this Terraform root.

Argo CD tracks application directories on main with auto-sync, prune, and self-heal. Installation and application onboarding are separate steps.

## Monitoring

[monitoring/helm.tf](monitoring/helm.tf) installs Prometheus, Grafana, Alertmanager, kube-state-metrics, and node exporter through kube-prometheus-stack. It configures persistent-volume claims for monitoring components.

NGINX ingress manifest files exist for Grafana and Prometheus under monitoring/ingress. Their presence does not prove they have been applied: the inspected installation workflow does not apply those files explicitly.

## Logging

[logging/main.tf](logging/main.tf) installs Loki and Fluent Bit. Fluent Bit runs as a DaemonSet, tails container logs, adds Kubernetes metadata, and sends data to Loki on port 3100.

Loki is configured as one SingleBinary replica with filesystem storage and authentication disabled. A ServiceMonitor is enabled in values, introducing a dependency on the relevant monitoring CRD. Review live persistence and retention before treating this as durable production logging.

## Service mesh

[service-mesh/helm.tf](service-mesh/helm.tf) installs Istio charts, configured at version 1.27.1. Other files define:

- Gateway: HTTP port 80 and configurable host.
- VirtualServices: application-prefix routing, rewrite, retry, timeout, and optional fault injection.
- DestinationRules: v1/v2 subsets, LEAST_REQUEST balancing, connection pools, and outlier detection.
- PeerAuthentication: application-selected mTLS, default STRICT.
- AuthorizationPolicy: optional ALLOW policy for requests from the configured application namespace.
- RequestAuthentication: optional JWT validation when issuer and JWKS URI are supplied.

JWT validation configuration alone is not a universal requirement that every request carry a token. Enforcement depends on the combined policies.

Source defaults assign primary v1 traffic 100% and canary v2 traffic 0%. The canary workflow creates a second deployment; traffic-shift and rollback workflows edit live VirtualServices directly.

### Ownership and removal boundaries

All mesh resources above share one root/state. The service-mesh-security workflow's destroy branch runs an unrestricted destroy in that root, so its scope includes mesh installation and routing, not only security policies.

Security/resilience workflows also apply the shared root. Direct traffic changes may be reconciled back to Terraform values. Verify sidecar injection and gateway reachability separately; merely installing policies does not demonstrate effective traffic protection.

The nested service-mesh/resilience directory is not called as a module by the parent root. Its standalone faultinjection.tf does not become active merely by existing there; the active parent routing.tf already contains fault configuration.

## DevSecOps storage

[devsecops/storage.tf](devsecops/storage.tf) creates a Storage Account and private containers for security reports, history, and SBOMs. RBAC and Key Vault files in that root are comments describing future work. The current scanner/report path is repository/artifact-based; container creation does not establish upload integration.

The separate addons/security and terraform/devsecops directories contain empty scaffolding in the inspected snapshot.

## Operational prerequisites

Core AKS must be available and credentials must permit each root's resources. Add-ons consume cluster capacity and can introduce CRD and storage dependencies. See the [workflow catalog](../../.github/workflows/README.md) for entry points; installation and removal workflows change resources.
