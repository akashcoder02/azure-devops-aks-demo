# GitHub Actions Workflow Catalog

[Project guide](../../docs/README.md)

The inspected repository contains 39 workflow YAML files. All expose workflow_dispatch. Build, direct deployment, GitOps deployment, and the consolidated security scan additionally expose workflow_call for reuse. The release workflow composes these reusable workflows.

These workflows do not automatically run on a normal documentation push in the inspected configuration. No workflow execution is required to read this guide.

## Workflow inventory

| File | Purpose | Effect |
|---|---|---|
| [infra.yaml](infra.yaml) | Provision core Azure platform and NGINX; create demo vault secret | Azure/Terraform changes |
| [destroy.yaml](destroy.yaml) | Destroy core platform | Destructive |
| [build.yaml](build.yaml) | Build SHA-tagged application image and push to ACR | Registry write |
| [release.yml](release.yml) | Coordinate build, optional security gate, and selected deployment | Release orchestration |
| [deploy.yml](deploy.yml) | Render and apply direct Kubernetes manifests | Cluster changes |
| [gitops-deploy.yml](gitops-deploy.yml) | Update desired manifests, create Argo Application if needed, verify rollout | Git and cluster changes |
| [gitops-rollback.yml](gitops-rollback.yml) | Select rollback image and commit desired deployment | Git changes and reconciliation |
| [gitops-scale.yml](gitops-scale.yml) | Commit desired replica count | Git changes and reconciliation |
| [rollback.yaml](rollback.yaml) | Set a selected image on a live deployment | Cluster changes |
| [scale.yaml](scale.yaml) | Scale live deployment | Cluster changes |
| [restart.yaml](restart.yaml) | Restart application deployment | Cluster changes |
| [undeploy-application.yml](undeploy-application.yml) | Delete application resources and Argo Application | Destructive |
| [canary-deployment.yml](canary-deployment.yml) | Create/version a canary deployment and verify rollout | Cluster changes |
| [traffic-shift.yml](traffic-shift.yml) | Edit and apply live VirtualService weights | Traffic changes |
| [rollback-traffic.yml](rollback-traffic.yml) | Restore live VirtualService traffic weights | Traffic changes |
| [install-argocd.yml](install-argocd.yml) | Install Argo CD and configure repository Secret | Terraform and cluster changes |
| [destroy-argocd.yml](destroy-argocd.yml) | Destroy Argo CD root | Destructive |
| [install-monitoring.yml](install-monitoring.yml) | Install monitoring stack | Terraform changes |
| [destroy-monitoring.yml](destroy-monitoring.yml) | Destroy monitoring root | Destructive |
| [logging.yml](logging.yml) | Install logging stack | Terraform changes |
| [destroy-logging.yml](destroy-logging.yml) | Destroy logging root | Destructive |
| [install-service-mesh.yml](install-service-mesh.yml) | Install Istio and mesh configuration | Terraform changes |
| [destroy-service-mesh.yml](destroy-service-mesh.yml) | Destroy service-mesh root | Destructive |
| [service-mesh-security.yml](service-mesh-security.yml) | Apply security inputs or destroy shared mesh root | Shared-root changes; destroy has broad scope |
| [service-mesh-resilience.yml](service-mesh-resilience.yml) | Apply resilience settings; optionally perform chaos actions | Terraform and possible disruptive cluster changes |
| [devsecops-install.yml](devsecops-install.yml) | Provision DevSecOps storage | Terraform changes |
| [devsecops-destroy.yml](devsecops-destroy.yml) | Destroy DevSecOps storage | Destructive |
| [security-scan.yml](security-scan.yml) | Run selected scanners, write/commit reports, upload artifacts | Report and Git writes |
| [gitleaks.yml](gitleaks.yml) | Standalone secrets scan and artifact upload | Runner reports/artifacts |
| [checkov.yml](checkov.yml) | Standalone IaC scan and artifact upload | Runner reports/artifacts |
| [trivy.yml](trivy.yml) | Standalone filesystem scan and artifact upload | Runner reports/artifacts |
| [aks-security.yml](aks-security.yml) | Collect AKS information into an artifact | Cloud query and artifact write |
| [azure-running-resources.yml](azure-running-resources.yml) | Inspect Azure resources and backend-related information | Diagnostic workflow |
| [images.yaml](images.yaml) | List ACR repositories/tags/image details | Diagnostic workflow |
| [logs.yaml](logs.yaml) | Read application logs | Diagnostic workflow |
| [platform-doctor.yaml](platform-doctor.yaml) | Inspect cluster, add-ons, ingress, metrics and events | Diagnostic workflow |
| [platform-status.yaml](platform-status.yaml) | Inspect Azure and Kubernetes platform status | Diagnostic workflow |
| [platform-installation-status.yml](platform-installation-status.yml) | Collect add-on status into a report artifact | Diagnostic and artifact write |
| [status-service-mesh.yml](status-service-mesh.yml) | Inspect Istio, routing, security and injection status | Diagnostic workflow |

## Release inputs

release.yml accepts application_name (tic-tac-toe or tetris), environment (development or production), deployment_strategy (traditional or gitops), deployment_type (default or hpa), and enable_devsecops.

The image tag is the initiating Git SHA. With DevSecOps enabled, security and release-gate jobs precede the selected deployment. Build success means the image was built/pushed, not that the application is serving traffic.

The direct-deployment workflow accepts deployment_type but does not implement the same HPA copy/remove mechanism used by GitOps.

## Credentials and contexts

Most cloud workflows use AZURE_CREDENTIALS with azure/login. Workflow files reference resource-name secrets such as RESOURCE_GROUP, AKS_CLUSTER, ACR_NAME, and KEYVAULT_NAME, while some steps retain literal names. GitOps writers use SSH_PRIVATE_KEY.

Review the exact selected YAML for its full environment/secret inputs. Terraform roots have independent provider/backend authentication needs. An Azure CLI login alone is not evidence that every provider or backend is correctly authenticated.

## Source, execution, and result

The portal's dispatch response reports whether GitHub accepted a request. The current portal status implementation looks up the latest repository run rather than a persisted per-request run ID.

GitOps deployment writes desired manifests to main. Security scanning writes reports to Git and uploads artifacts. Diagnostic workflows still execute on runners and may create artifacts or update runner kubeconfig; they are not equivalent to passive repository reads.

## Operational boundaries

- Destroy Platform removes resources; it does not suspend them.
- Service Mesh Security destroy operates on the entire shared service-mesh Terraform root.
- Traffic shift and traffic rollback edit live resources also declared by Terraform.
- Direct rollback and scale can conflict with Argo CD ownership.
- Some checks tolerate failure. Read the job's actual steps and results rather than treating a summary banner as complete evidence.
- The current release gate does not explicitly download the current scan artifacts into its job.
- Current workflows target a shared default deployment structure, not independently isolated environments.

See [security](../../app/security/README.md), [GitOps](../../gitops/README.md), and [add-ons](../../terraform/addons/README.md) for those details.
