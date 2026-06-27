#!/bin/bash

set -e

source scripts/lib/config.sh
source scripts/lib/common.sh

clear

echo "========================================"
echo " Azure DevOps Demo - Shutdown Script"
echo "========================================"

echo ""
echo "The following resources will be destroyed:"
echo ""
echo "  - AKS Cluster"
echo "  - Azure Container Registry"
echo "  - Resource Group"
echo ""
echo "Terraform Backend Storage Account will NOT be deleted."
echo ""

read -p "Do you really want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    info "Shutdown cancelled."
    exit 0
fi

info "Moving to Terraform directory..."

cd "$TERRAFORM_DIR"

info "Destroying infrastructure..."

terraform destroy -auto-approve

cd ..

success "Infrastructure destroyed successfully."

echo ""
echo "Verifying resources..."

if az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
    error "Resource Group still exists!"
else
    success "Resource Group deleted."
fi

echo ""
echo "========================================"
echo " Environment Shutdown Complete"
echo "========================================"

echo ""
echo "Backend Storage Account:"
echo "   Preserved"

echo ""
echo "Terraform State:"
echo "   Preserved"

echo ""
echo "Good Night! 😴"
