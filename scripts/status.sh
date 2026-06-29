#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/lib/config.sh"

clear

echo "========================================"
echo " Azure DevOps Demo - Platform Status"
echo "========================================"

echo ""

#########################################
# Azure Status
#########################################

if az account show >/dev/null 2>&1
then
    echo "AZURE=CONNECTED"
else
    echo "AZURE=NOT_CONNECTED"
fi

echo "RESOURCE_GROUP=$RESOURCE_GROUP"
echo "LOCATION=$LOCATION"

echo ""

#########################################
# Terraform Status
#########################################

if command -v terraform >/dev/null 2>&1
then

    if command -v jq >/dev/null 2>&1
    then
        TF_VERSION=$(terraform version -json | jq -r '.terraform_version')
    else
        TF_VERSION=$(terraform version | head -1)
    fi

    echo "TERRAFORM_STATUS=READY"
    echo "TERRAFORM_VERSION=$TF_VERSION"
    echo "TERRAFORM_BACKEND=Azure Blob"

else

    echo "TERRAFORM_STATUS=NOT_INSTALLED"
    echo "TERRAFORM_VERSION=-"
    echo "TERRAFORM_BACKEND=-"

fi

echo ""

#########################################
# Docker Status
#########################################

if docker info >/dev/null 2>&1
then
    echo "DOCKER=RUNNING"
else
    echo "DOCKER=STOPPED"
fi

echo ""

#########################################
# Kubernetes Status
#########################################

echo "AKS_NAME=$AKS_NAME"

if kubectl get nodes >/dev/null 2>&1
then

    echo "AKS=RUNNING"

    CLUSTER=$(kubectl config current-context)

    echo "CLUSTER=$CLUSTER"

    NODES=$(kubectl get nodes --no-headers | wc -l)

    echo "NODES=$NODES"

    PODS=$(kubectl get pods -A --no-headers | wc -l)

    echo "PODS=$PODS"

    NAMESPACE=$(kubectl config view --minify --output 'jsonpath={..namespace}')

    if [ -z "$NAMESPACE" ]
    then
        NAMESPACE=default
    fi

    echo "NAMESPACE=$NAMESPACE"

else

    echo "AKS=STOPPED"
    echo "CLUSTER=Offline"
    echo "NODES=0"
    echo "PODS=0"
    echo "NAMESPACE=-"

fi

echo ""

#########################################
# Azure Container Registry
#########################################

echo "ACR_NAME=$ACR_NAME"
echo "ACR_LOGIN_SERVER=${ACR_NAME}.azurecr.io"

if az acr show --name "$ACR_NAME" >/dev/null 2>&1
then
    echo "ACR_STATUS=CONNECTED"
else
    echo "ACR_STATUS=NOT_CONNECTED"
fi

echo ""

#########################################
# Platform Summary
#########################################

echo "========================================"
echo " Platform Status Complete"
echo "========================================"