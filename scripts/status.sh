#!/bin/bash

source scripts/lib/config.sh

#########################################
# Docker
#########################################

if docker info >/dev/null 2>&1
then
    echo "DOCKER=RUNNING"
else
    echo "DOCKER=STOPPED"
fi

#########################################
# Kubernetes
#########################################

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


#########################################
# Azure
#########################################

if az account show >/dev/null 2>&1
then
    echo "AZURE=CONNECTED"
else
    echo "AZURE=NOT_CONNECTED"
fi

#########################################
# Azure Container Registry
#########################################

echo "ACR_NAME=$ACR_NAME"

if az acr show --name "$ACR_NAME" >/dev/null 2>&1
then
    echo "ACR_STATUS=CONNECTED"
else
    echo "ACR_STATUS=NOT_CONNECTED"
fi

#########################################
# Terraform
#########################################

if command -v terraform >/dev/null 2>&1
then

    TF_VERSION=$(terraform version -json 2>/dev/null | jq -r '.terraform_version')

    echo "TERRAFORM_STATUS=READY"

    echo "TERRAFORM_VERSION=$TF_VERSION"

    echo "TERRAFORM_BACKEND=Azure Blob"

else

    echo "TERRAFORM_STATUS=NOT_INSTALLED"

    echo "TERRAFORM_VERSION=-"

    echo "TERRAFORM_BACKEND=-"

fi