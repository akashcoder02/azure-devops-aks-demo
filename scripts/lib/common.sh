#!/bin/bash

info() {
    echo ""
    echo "[INFO] $1"
}

success() {
    echo ""
    echo "[SUCCESS] $1"
}

error() {
    echo ""
    echo "[ERROR] $1"
    exit 1
}
check_azure() {

    printf "%-35s" "Azure Login"

    if az account show >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
	return 1
    fi
}

check_backend() {

    printf "%-35s" "Terraform Backend"

    if [ -f terraform/.terraform/terraform.tfstate ]
    then
        echo "✅"
    else
        echo "❌"
    fi
}

check_resource_group() {

    printf "%-35s" "Resource Group"

    if az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_aks() {

    printf "%-35s" "AKS Cluster"

    if az aks show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AKS_NAME" >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_kubectl() {

    printf "%-35s" "kubectl"

    if kubectl cluster-info >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_acr() {

    printf "%-35s" "Azure Container Registry"

    if az acr show \
        --name "$ACR_NAME" >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_local_image() {

    printf "%-35s" "Local Docker Image"

    if docker image inspect ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_acr_image() {

    printf "%-35s" "ACR Docker Image"

    if az acr repository show-tags \
        --name "$ACR_NAME" \
        --repository "$IMAGE_NAME" \
        --output tsv 2>/dev/null | grep -q "^${IMAGE_TAG}$"
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_helm() {

    printf "%-35s" "Helm Release"

    if helm status "$HELM_RELEASE" >/dev/null 2>&1
    then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_pods() {

    printf "%-35s" "Pods"

    RUNNING=$(kubectl get pods --no-headers 2>/dev/null | grep Running | wc -l)

    if [ "$RUNNING" -gt 0 ]
    then
        echo "✅ ($RUNNING Running)"
        return 0
    else
        echo "❌"
        return 1
    fi
}

check_service() {

    printf "%-35s" "Service"

    if kubectl get svc ${HELM_RELEASE}-service >/dev/null 2>&1
    then

        IP=$(kubectl get svc ${HELM_RELEASE}-service \
            -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

        echo "✅ ${IP:-Pending}"
        return 0

    else

        echo "❌"
        return 1

    fi
}
