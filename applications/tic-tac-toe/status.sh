#!/bin/bash

set -e

API_MODE=false

if [ "$1" = "--api" ]
then
    API_MODE=true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source ../../platform/config/platform.env
source app.env

if [ "$API_MODE" = false ]
then
    clear
fi

if [ "$API_MODE" = false ]
then

    echo "========================================"
    echo " Tic Tac Toe - Application Status"
    echo "========================================"

    echo ""
    echo "Application : $APP_NAME"
    echo ""

fi

#########################################
# Validate Platform
#########################################

if [ "$API_MODE" = false ]
then

    echo "[1/4] Validating Platform..."

fi

if ! kubectl get nodes >/dev/null 2>&1
then

    if [ "$API_MODE" = true ]
    then
        echo "STATUS=PLATFORM_DOWN"
    else
        echo "❌ AKS Cluster is unavailable."
    fi

    exit 1

fi

if [ "$API_MODE" = false ]
then
    echo "✓ Platform Ready"
fi

#########################################
# Deployment Status
#########################################

if [ "$API_MODE" = false ]
then

    echo ""
    echo "[2/4] Deployment Status..."

fi

if kubectl get deployment "$DEPLOYMENT_NAME" >/dev/null 2>&1
then

    READY=$(kubectl get deployment "$DEPLOYMENT_NAME" \
        -o jsonpath='{.status.readyReplicas}')

    REPLICAS=$(kubectl get deployment "$DEPLOYMENT_NAME" \
        -o jsonpath='{.status.replicas}')

    IMAGE=$(kubectl get deployment "$DEPLOYMENT_NAME" \
        -o jsonpath='{.spec.template.spec.containers[0].image}')

    READY=${READY:-0}
    REPLICAS=${REPLICAS:-0}

    echo "DEPLOYMENT=RUNNING"
    echo "READY=$READY/$REPLICAS"
    echo "IMAGE=$IMAGE"

else

    echo "DEPLOYMENT=NOT_DEPLOYED"

fi

#########################################
# Service Status
#########################################

if [ "$API_MODE" = false ]
then

    echo ""
    echo "[3/4] Service Status..."

fi

if kubectl get service "$SERVICE_NAME" >/dev/null 2>&1
then

    echo "SERVICE=RUNNING"

    EXTERNAL_IP=$(kubectl get svc "$SERVICE_NAME" \
        -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

    if [ -z "$EXTERNAL_IP" ]
    then
        EXTERNAL_IP="Pending"
    fi

    echo "EXTERNAL_IP=$EXTERNAL_IP"

else

    echo "SERVICE=NOT_FOUND"
    EXTERNAL_IP=""

fi

#########################################
# Pod Status
#########################################

if [ "$API_MODE" = false ]
then

    echo ""
    echo "[4/4] Pod Status..."

fi

PODS=$(kubectl get pods \
    -l app=$DEPLOYMENT_NAME \
    --no-headers 2>/dev/null | wc -l)

echo "PODS=$PODS"

echo ""

echo "========================================"
echo " Application Status"
echo "========================================"

echo ""

echo "Application : $APP_NAME"
echo "Namespace   : $NAMESPACE"

if [ -n "$EXTERNAL_IP" ] && [ "$EXTERNAL_IP" != "Pending" ]
then

    echo "URL=http://$EXTERNAL_IP"

else

    echo "URL=-"

fi

echo ""

echo "✓ Status check completed."