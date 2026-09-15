# Sample Applications

[Project guide](../docs/README.md) · [GitOps](../gitops/README.md)

The current release workflow supports two applications. They demonstrate delivery mechanisms rather than a multi-service business backend.

| Application | Runtime | Container port | Service port | URL prefix |
|---|---|---|---|---|
| Tetris | Static HTML/CSS/JavaScript served by nginx:alpine | 80 | 80 | /tetris |
| Tic-Tac-Toe | Flask and browser JavaScript | 5001 | 80 | /tic-tac-toe |

## Source and packaging

[tetris](tetris) contains the game, Dockerfile, Kubernetes manifests, and its original README. Game state is handled in browser code.

[tic-tac-toe/app.py](tic-tac-toe/app.py) renders a game page and uses ProxyFix for the forwarded URL prefix. Its Dockerfile uses Python 3.12 slim and starts Flask directly with debug enabled. This is a demo runtime, not a hardened production web-server setup.

Neither application defines a persistent business database.

## Build and deployment

The reusable build workflow takes application_name, builds the corresponding directory, tags the image with the Git SHA, and pushes it to ACR.

Two manifest sets serve different purposes:

| Path | Purpose |
|---|---|
| applications/<name>/k8s | Direct deployment templates; image/identity placeholders are rendered by workflows |
| gitops/applications/<name> | Committed desired state reconciled by Argo CD |

Do not assume the files in both locations remain synchronized automatically.

Current GitOps deployments request 100m CPU and 128Mi memory and limit usage to 500m CPU and 512Mi memory. Both desired deployments currently declare one replica and version v1. These are source values, not live replica counts.

## Ingress

NGINX uses regex paths and prefix rewriting to send requests to the application Services. Development core configuration uses a ClusterIP ingress controller; production selects LoadBalancer. Istio provides a separate configured gateway/routing path.

Ingress existence, external addressing, sidecars, and actual HTTP availability must be verified against the intended runtime.

## Key Vault example

Tic-Tac-Toe mounts a secrets-store CSI volume at /mnt/secrets-store. The SecretProviderClass requests app-secret from Azure Key Vault using the AKS secrets-provider managed identity. Workflows populate the identity placeholder or update the tracked identity value.

The inspected Flask app does not read that mounted secret. The integration demonstrates mounting infrastructure; it does not establish that game behavior depends on Key Vault data.

## Local scripts and extension

Tic-Tac-Toe includes deploy.sh, status.sh, and undeploy.sh. Their local flow differs from the GitHub workflows, including manifest coverage and working-directory assumptions. Tetris does not have equivalent local lifecycle scripts.

Adding an application currently requires more than creating a folder: review workflow choices, portal catalog entries, Kubernetes manifests, GitOps Application definitions, optional HPA configuration, mesh application settings, and report scanner paths.

A future catalog-driven onboarding process could reduce these repeated edits. It is not implemented by this documentation.
