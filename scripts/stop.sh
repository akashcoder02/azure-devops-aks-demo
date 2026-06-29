#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/lib/config.sh"
source "$SCRIPT_DIR/lib/common.sh"

clear

echo "========================================"
echo " Azure DevOps Demo - Stop Platform"
echo "========================================"

echo ""

#########################################
# Validate Azure Login
#########################################

echo "[1/5] Validating Azure Login..."

if ! az account show >/dev/null 2>&1
then
    error "Azure CLI is not logged in."
    exit 1
fi

success "Azure Login OK"

#########################################
# Verify Terraform Directory
#########################################

echo ""
echo "[2/5] Preparing Terraform..."

cd "$TERRAFORM_DIR"

terraform init

success "Terraform Initialized."

#########################################
# Destroy Infrastructure
#########################################

echo ""
echo "[3/5] Destroying Infrastructure..."

terraform destroy -auto-approve

success "Terraform Destroy Completed."

cd ..

#########################################
# Verify Resources Removed
#########################################

echo ""
echo "[4/5] Verifying Azure Resources..."

RG_EXISTS=$(az group exists --name "$RESOURCE_GROUP")

if [ "$RG_EXISTS" = "true" ]
then
    error "Resource Group still exists."
    exit 1
fi

success "Resource Group deleted."

#########################################
# Completed
#########################################

echo ""
echo "[5/5] Platform Stopped"

echo ""

echo "========================================"
echo " Platform Destroyed"
echo "========================================"

echo ""

echo "Azure Resources : Removed"

echo "Terraform State : Updated"

echo ""

success "Platform shutdown completed successfully."
