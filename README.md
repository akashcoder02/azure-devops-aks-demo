# Azure DevOps AKS Platform

A production-style Azure DevOps Platform built on Microsoft Azure using Terraform, Azure Kubernetes Service (AKS), Azure Container Registry (ACR), Azure Key Vault, GitHub Actions, Docker, Kubernetes and Argo CD.

This project demonstrates Infrastructure as Code (IaC), CI/CD, GitOps deployment, Kubernetes operations and Azure cloud automation.

---

# Features

## Infrastructure Automation

- Infrastructure as Code using Terraform
- Azure Resource Group
- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Azure Key Vault
- Azure Storage Backend for Terraform State
- RBAC Role Assignments
- Modular Terraform Architecture

---

## CI/CD

- GitHub Actions
- Docker Image Build
- Azure Container Registry Push
- Traditional Kubernetes Deployment
- GitOps Deployment
- Release Pipeline

---

## GitOps

- Argo CD Installation
- Git Repository Integration
- Automatic Synchronization
- Declarative Kubernetes Deployments

---

## Kubernetes Operations

- Deploy Applications
- Restart Application
- Rollback Deployment
- Scale Application
- View Application Logs
- Health Check
- Platform Status

---

## Monitoring

- Azure Resource Audit
- Running Resource Detection
- Cost Resource Detection
- Docker Image Listing

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Cloud | Microsoft Azure |
| IaC | Terraform |
| Container | Docker |
| Container Registry | Azure Container Registry |
| Orchestration | Kubernetes |
| Kubernetes Service | Azure AKS |
| Secrets | Azure Key Vault |
| GitOps | Argo CD |
| CI/CD | GitHub Actions |
| Language | Python |
| Web Framework | Flask |
| OS | Ubuntu |
| Shell | Bash |

---

# Architecture

```
Developer
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions
      │
      ├──────────────► Docker Build
      │
      ├──────────────► Push Image to ACR
      │
      ▼
GitOps Deploy
      │
      ▼
Git Repository Update
      │
      ▼
Argo CD
      │
      ▼
Azure Kubernetes Service
      │
      ▼
Application
```

---

# Repository Structure

```
terraform/
│
├── modules/
├── addons/
│   └── argocd/
├── backend/
├── main.tf
├── providers.tf
└── outputs.tf

applications/
├── tic-tac-toe/
└── tetris/

gitops/
├── applications/
└── projects/

scripts/

platform/

app/
```

---

# Infrastructure Components

- Azure Resource Group
- Azure Kubernetes Service
- Azure Container Registry
- Azure Key Vault
- Azure Storage Account
- Azure Role Assignments

---

# GitHub Actions Workflows

## Platform

- Platform Infrastructure
- Destroy Platform
- Platform Status

---

## Build

- Build Docker Image

---

## Deployment

- Release Application
- Deploy to AKS
- GitOps Deploy

---

## GitOps

- Install Argo CD
- Destroy Argo CD

---

## Operations

- Restart Application
- Scale Application
- Rollback Deployment
- Application Logs
- Application Health Check

---

## Monitoring

- Azure Running Resources
- List Docker Images

---

# Deployment Flow

## Platform Creation

```
Platform Infrastructure
        │
        ▼
Terraform
        │
        ▼
Azure Resources Created
        │
        ▼
AKS Ready
```

---

## GitOps Setup

```
Install Argo CD
        │
        ▼
Terraform
        │
        ▼
Argo CD Installed
        │
        ▼
Git Repository Connected
```

---

## Release Flow

```
Release Application
        │
        ▼
Build Docker Image
        │
        ▼
Push Image to ACR
        │
        ▼
GitOps Deploy
        │
        ▼
Update Deployment Manifest
        │
        ▼
Commit to Git
        │
        ▼
Argo CD Synchronization
        │
        ▼
Application Running
```

---

# Applications

Current sample applications included in this repository:

- Tic-Tac-Toe
- Tetris

Each application contains:

- Dockerfile
- Kubernetes Manifests
- GitOps Manifests
- Service
- Ingress

---

# Security

- Azure Service Principal Authentication
- Azure Key Vault Integration
- Managed Identity
- Kubernetes SecretProviderClass
- GitHub Secrets
- SSH Authentication

---

# Terraform Modules

- Resource Group
- AKS
- ACR
- Key Vault
- Network

---

# Supported Operations

- Create Platform
- Destroy Platform
- Install Argo CD
- Deploy Application
- GitOps Deployment
- Restart
- Rollback
- Scale
- View Logs
- Health Check
- Platform Status
- Azure Resource Audit

---

# Future Enhancements

- Azure Functions
- Azure Logic Apps
- Datadog Integration
- Prometheus
- Grafana
- Horizontal Pod Autoscaler
- Multiple Environments
- Multi-Cluster Deployment

---

# Author

Akash Goylit

Azure DevOps | Azure Cloud | Terraform | Kubernetes | Docker | GitHub Actions | GitOps | Argo CD

---

# License

This project is intended for learning, demonstration and portfolio purposes.