# GitOps Delivery

[Project guide](../docs/README.md) · [Applications](../applications/README.md)

## Layout

| Directory | Role |
|---|---|
| applications/tetris | Tetris desired Deployment, Service, and Ingress |
| applications/tic-tac-toe | Tic-Tac-Toe desired resources plus SecretProviderClass |
| projects | Argo CD Application resources; despite the folder name, these are not AppProject definitions |
| addons/hpa | Optional HPA templates copied into application directories by deployment automation |

## Argo CD configuration

Each Application watches this repository's main branch at its own gitops/applications path, deploys to the local Kubernetes cluster's default namespace, and uses the default Argo CD project.

Automated sync enables prune and selfHeal, with CreateNamespace=true. A manifest removed from the watched path may be pruned; direct edits to managed resources may be undone.

## GitOps release flow

1. Build and publish an image to ACR.
2. Authenticate to GitHub over SSH and to Azure through workflow credentials.
3. Check the cluster/image and resolve the Key Vault identity when required.
4. Update the desired image and identity fields.
5. Apply the selected deployment mode to the Git working copy.
6. Commit and push changes to main.
7. Create the Argo CD Application if missing.
8. Wait for sync and deployment rollout.
9. Attempt to append and commit deployment history.

This is a hybrid bootstrap flow: application desired state lives in Git, but the workflow still connects to AKS to create the Argo CD Application and verify runtime state.

## Autoscaling

[scripts/deployment/deployment-mode.sh](../scripts/deployment/deployment-mode.sh) copies the HPA template into the watched application directory when hpa is selected; default mode removes that file.

Both HPA templates target CPU utilization of 70%, with minimum two and maximum ten replicas. In the inspected snapshot neither watched application directory contains an hpa.yaml, so the template files alone do not enable Argo CD-managed HPAs.

Deployment replica fields remain present in desired manifests. HPA and GitOps replica ownership should be reviewed before relying on autoscaling; the Application definitions do not declare replica ignore rules.

## Rollback and scale

GitOps rollback selects an image tag, changes the deployment manifest, and pushes it. GitOps scale changes the replicas value and pushes it. Traditional rollback/scale workflows instead change the live cluster.

Choose operations consistent with ownership. Live changes to the same Argo CD-managed resources can be reverted by self-healing.

## Boundaries

There are no separate development/production overlay trees. Both applications use main and default namespace. SSH credentials must permit the intended repository writes. Concurrent workflow commits may conflict or race; successful sync status alone should not be substituted for checking the intended image and revision.

Mesh routing is managed outside these application paths. See [add-on ownership](../terraform/addons/README.md).
