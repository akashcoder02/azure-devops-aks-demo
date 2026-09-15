# Local Scripts and Helpers

[Project guide](../docs/README.md) · [Workflow catalog](../.github/workflows/README.md)

These scripts are local automation, separate from GitHub-hosted workflow execution. The portal's local job services can invoke some of them. Read a script before executing it; names such as start and stop refer to infrastructure lifecycle.

| File | Purpose | Effect |
|---|---|---|
| [start.sh](start.sh) | Check Azure login, initialize/plan/apply Terraform, obtain AKS credentials, validate platform | Provisions resources and updates local context |
| [stop.sh](stop.sh) | Initialize Terraform and destroy the platform | Destructive |
| [status.sh](status.sh) | Inspect Azure login, tools, cluster, namespace, and ACR | Status queries |
| [doctor.sh](doctor.sh) | Check tools, authentication, cluster, and registry | Diagnostic queries |
| [git-push.sh](git-push.sh) | Git publishing helper | Can write repository history/remotes |
| [deployment/deployment-mode.sh](deployment/deployment-mode.sh) | Copy/remove HPA manifest in GitOps application path | Modifies local desired-state files |
| [add_scan_time.py](add_scan_time.py) | Normalize report content and add scan timestamp | Writes report file |
| [merge_kubernetes_reports.py](merge_kubernetes_reports.py) | Merge Kubernetes scanner report inputs | Writes report output |
| [lib/config.sh](lib/config.sh) | Older shared resource/image/chart settings | Configuration |
| [lib/common.sh](lib/common.sh) | Output and status helpers | Shared functions |

## Working directories

start.sh sources paths relative to the repository root. Other scripts resolve paths from their own location. Portal job managers and script_runner do not all use the same execution directory, so local invocation and portal invocation should not be assumed equivalent.

The Terraform environment input has no default in the core root, while start.sh does not explicitly supply it. A noninteractive invocation needs an intentional input strategy; this guide does not claim the script is unattended-ready.

## Two configuration sources

scripts/lib/config.sh includes older flask-demo image and Helm release defaults. platform/config/platform.env is used by other parts of the platform. These are separate files, not automatically synchronized configuration.

## Application scripts

Tic-Tac-Toe has separate deploy, status, and undeploy scripts in [applications/tic-tac-toe](../applications/tic-tac-toe). Their relative paths and resource coverage differ from the GitHub workflows. Tetris does not provide the same local script set.

The portal also references create-vm.sh, which is not present in scripts/. The VM action is therefore incomplete in the inspected snapshot.

## Recovery and evidence

Review command return codes and actual resources when diagnosing failure. Some helpers combine output or return coarse status values. The portal's shared job record is in memory, so it is not a durable operational audit log.
