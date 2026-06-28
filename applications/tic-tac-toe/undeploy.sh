#!/bin/bash

set -e

source ../../platform/config/platform.env
source app.env

clear

echo "========================================"
echo " Tic Tac Toe - Undeploy"
echo "========================================"

echo ""
echo "Application : $APP_NAME"
echo ""

#########################################
# Validate Platform
#########################################

echo "[1/4] Validating Platform..."

if ! az account show >/dev/null 2>&1
then
    echo "❌ Azure is not logged in."
    exit 1
fi

if ! kubectl get nodes >/dev/null 2>&1
then
    echo "❌ AKS Cluster is unavailable."
    exit 1
fi

echo "✓ Platform Ready"

#########################################
# Delete Kubernetes Resources
#########################################

echo ""
echo "[2/4] Removing Application..."

kubectl delete deployment ${DEPLOYMENT_NAME} \
    --ignore-not-found

kubectl delete service ${SERVICE_NAME} \
    --ignore-not-found

echo "✓ Kubernetes resources removed."

#########################################
# Verify Removal
#########################################

echo ""
echo "[3/4] Verifying..."

kubectl get deployments

echo ""

kubectl get services

#########################################
# Completed
#########################################

echo ""
echo "[4/4] Completed"

echo ""

echo "========================================"
echo " Application Removed"
echo "========================================"

echo ""

echo "Application : $APP_NAME"

echo "Namespace   : $NAMESPACE"

echo ""

echo "✓ Undeploy completed successfully."
