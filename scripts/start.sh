#!/bin/bash

set -e
source scripts/lib/config.sh
source scripts/lib/common.sh

echo "========================================"
echo " Azure DevOps Demo - Startup Script"
echo "========================================"

echo ""
echo "[1/5] Checking Azure Login..."

if ! az account show >/dev/null 2>&1; then
    az login
fi

echo "Azure Login OK"

echo ""
echo "[2/5] Provisioning Azure Infrastructure..."

cd "$PROJECT_ROOT/terraform"

terraform init

echo ""
info "Checking Terraform changes..."

terraform plan -out=tfplan

if terraform show -no-color tfplan | grep -q "No changes."; then
    success "Terraform infrastructure already up-to-date."
else
    info "Applying Terraform changes..."
    terraform apply -auto-approve tfplan
fi

cd ..

echo ""
echo "[3/5] Getting AKS Credentials..."

az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_NAME \
  --overwrite-existing

mkdir -p ~/.kube
cp /mnt/c/Users/Asus/.kube/config ~/.kube/config
chmod 600 ~/.kube/config

echo ""
echo "[4/5] Waiting for AKS Node..."

kubectl wait \
  --for=condition=Ready node \
  --all \
  --timeout=600s

info "Verifying AKS access to ACR..."

if az aks check-acr \
    --resource-group "$RESOURCE_GROUP" \
    --name "$AKS_NAME" \
    --acr "${ACR_NAME}.azurecr.io" >/dev/null 2>&1
then
    success "AKS can pull images from ACR."
else
    error "AKS cannot pull images from ACR."
fi

#########################################
# Platform Validation
#########################################

echo ""
echo "[5/5] Validating Platform..."

echo ""

info "Checking Kubernetes Nodes..."

kubectl get nodes

echo ""

info "Checking System Pods..."

kubectl get pods -A

echo ""

info "Checking Azure Container Registry..."

az acr show \
    --name "$ACR_NAME" \
    --resource-group "$RESOURCE_GROUP" >/dev/null

success "Azure Container Registry Ready."

echo ""

echo "========================================"
echo " Platform Ready"
echo "========================================"

echo ""

echo "Azure Login       : OK"
echo "Terraform         : OK"
echo "Resource Group    : $RESOURCE_GROUP"
echo "AKS Cluster       : $AKS_NAME"
echo "Azure ACR         : $ACR_NAME"

echo ""

success "Platform provisioned successfully."