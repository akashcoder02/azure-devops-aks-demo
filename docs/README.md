# Azure DevOps AKS Platform — Project Guide

This repository implements an Internal Developer Platform (IDP) prototype for Azure application delivery. A Flask portal brings together GitHub Actions, Terraform, AKS, ACR, Key Vault, Argo CD, monitoring, logging, and Istio controls.

This guide documents the implementation inspected at commit `a1e6a68e9d2829832cc6f741002776fefe1b70ae`. It describes repository configuration, not a verified live Azure installation. Existing root and component READMEs are preserved.

## Start here

| Guide | What it explains |
|---|---|
| [Architecture](architecture/README.md) | Components, execution paths, ownership, and state |
| [Developer portal](../app/README.md) | Flask application, routes, runtime requirements, and integrations |
| [Terraform foundation](../terraform/README.md) | Azure resources, backend, identities, and environment behavior |
| [Platform add-ons](../terraform/addons/README.md) | Argo CD, monitoring, logging, Istio, and DevSecOps storage |
| [Applications](../applications/README.md) | Tetris, Tic-Tac-Toe, containers, ingress, and secrets |
| [GitOps](../gitops/README.md) | Argo CD reconciliation, deployment manifests, and autoscaling |
| [Workflow catalog](../.github/workflows/README.md) | All 39 workflows and their operational effects |
| [Local scripts](../scripts/README.md) | Local lifecycle commands and helper scripts |
| [Shared configuration](../platform/README.md) | Platform configuration and portability boundaries |
| [Security implementation](../app/security/README.md) | Scanners, report parsing, scoring, and policy limitations |
| [Reports](../reports/README.md) | Report formats, provenance, and freshness |
| [Deployment history](../history/README.md) | CSV records and history consumers |
| [Flask Helm chart](../flask-demo/README.md) | Separate chart and its relationship to current releases |

## What the platform does

- Provisions a core Azure environment with Terraform.
- Builds sample application containers and publishes images to ACR.
- Supports direct Kubernetes deployment and GitOps deployment.
- Offers release, rollback, scale, restart, and diagnostic workflows.
- Installs observability and service-mesh add-ons independently.
- Presents infrastructure inventory and stored security findings in a portal.

The project is useful for learning, demonstrations, and evaluating internal self-service workflows. Production readiness, availability, customer isolation, and reliable security enforcement are not established by the source alone.

## Logical setup order

1. Establish the intended Azure account, resource names, permissions, and Terraform state backend.
2. Provision the core platform: resource group, AKS, ACR, Key Vault, role assignments, and NGINX ingress.
3. Install Argo CD if using GitOps. Install monitoring, logging, and Istio only when needed.
4. Configure the portal host and GitHub workflow credentials.
5. Build and deploy one sample application using the selected deployment strategy.
6. Inspect deployment status, image identity, ingress, and application behavior.
7. Exercise recovery only within the intended test environment.

This is an architectural sequence, not a command script. The platform's Start, Stop, Install, Release, and Destroy actions can change Azure or Kubernetes resources. In particular, Stop destroys infrastructure rather than suspending an AKS cluster. Consult the component guides before operating these actions.

## Current boundaries

The application catalog is centered on two named applications. Development and production share the same configuration structure and default resource names; the environment input is not a separate tenant or cluster boundary. Some modules, pages, and helper files are empty or incomplete. Status labels can combine live queries with assumptions or placeholders.

The main operational concerns are portal access control, durable job tracking, configuration ownership across Terraform and direct Kubernetes operations, and tying release decisions to fresh security evidence. These are documented where they occur rather than represented as completed capabilities.

## Suggested demonstration

Explain one application from source to ACR, then through a chosen deployment strategy to AKS. Show the exact workflow and desired manifest, application status, and how rollback is intended to work. Explain the difference between stored security results and live status. Present measured outcomes only after an actual controlled test.
