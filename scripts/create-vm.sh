#!/bin/bash

set -e

VM_NAME="$1"
VM_COUNT="$2"
VM_TEMPLATE="$3"
LOCATION="$4"
VM_SIZE="$5"
ADMIN_USERNAME="$6"
PUBLIC_KEY="$7"

WORKLOAD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../terraform/workloads/vm" && pwd)"

cd "$WORKLOAD_DIR"

echo "=========================================="
echo "Azure IDP - VM Provisioning"
echo "=========================================="
echo "VM Name        : $VM_NAME"
echo "Terraform VM Name: '$VM_NAME'"
echo "VM Count       : $VM_COUNT"
echo "Template       : $VM_TEMPLATE"
echo "VM Size        : $VM_SIZE"
echo "Admin Username : $ADMIN_USERNAME"
echo "Location       : $LOCATION"
echo "=========================================="

cat > terraform.auto.tfvars <<EOF
subscription_id = "3a15b2d9-99f7-48fa-a6c6-9ebd7ff7a153"

resource_group_name = "rg-devops-demo"

location = "Central India"

vnet_name = "idp-vnet"

subnet_name = "idp-subnet"

vm_name = "$VM_NAME"

vm_count = $VM_COUNT

vm_size = "$VM_SIZE"

admin_username = "$ADMIN_USERNAME"

public_key = "$PUBLIC_KEY"

os_disk_size_gb = 64

public_ip_enabled = true
EOF

echo
echo "Running Terraform Init..."
terraform init

echo
echo "Running Terraform Apply..."
terraform apply -auto-approve

echo
echo "=========================================="
echo "Provisioning Completed"
echo "=========================================="

terraform output