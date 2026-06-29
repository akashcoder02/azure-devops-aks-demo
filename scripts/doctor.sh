#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/lib/config.sh"
source "$SCRIPT_DIR/lib/common.sh"

clear

echo "========================================"
echo " Azure DevOps Demo - Platform Doctor"
echo "========================================"

echo ""

#########################################
# Check Azure CLI
#########################################

echo "[1/8] Azure CLI"

if command -v az >/dev/null 2>&1
then
    success "Azure CLI Installed."
else
    error "Azure CLI is not installed."
    exit 1
fi

#########################################
# Check Azure Login
#########################################

echo ""
echo "[2/8] Azure Login"

if az account show >/dev/null 2>&1
then
    success "Azure Login OK."
else
    error "Not logged into Azure."
fi

#########################################
# Check Terraform
#########################################

echo ""
echo "[3/8] Terraform"

if command -v terraform >/dev/null 2>&1
then

    VERSION=$(terraform version | head -1)

    success "$VERSION"

else

    error "Terraform is not installed."

fi

#########################################
# Check Docker
#########################################

echo ""
echo "[4/8] Docker"

if command -v docker >/dev/null 2>&1
then
    success "Docker Installed."
else
    error "Docker is not installed."
fi

#########################################
# Check Docker Daemon
#########################################

echo ""
echo "[5/8] Docker Engine"

if docker info >/dev/null 2>&1
then
    success "Docker Engine Running."
else
    error "Docker Engine Stopped."
fi

#########################################
# Check kubectl
#########################################

echo ""
echo "[6/8] kubectl"

if command -v kubectl >/dev/null 2>&1
then

    VERSION=$(kubectl version --client --short 2>/dev/null || kubectl version --client)

    success "$VERSION"

else

    error "kubectl is not installed."

fi

#########################################
# Check AKS
#########################################

echo ""
echo "[7/8] Kubernetes"

if kubectl get nodes >/dev/null 2>&1
then

    NODE_COUNT=$(kubectl get nodes --no-headers | wc -l)

    success "AKS Reachable."

    echo "Nodes : $NODE_COUNT"

else

    error "AKS Cluster is unavailable."

fi

#########################################
# Check Azure Container Registry
#########################################

echo ""
echo "[8/8] Azure Container Registry"

if az acr show --name "$ACR_NAME" >/dev/null 2>&1
then

    success "ACR Available."

else

    error "ACR Not Found."

fi

#########################################
# Summary
#########################################

echo ""
echo "========================================"
echo " Platform Health Check Complete"
echo "========================================"

echo ""

success "Doctor finished."