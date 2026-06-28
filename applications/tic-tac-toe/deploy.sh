#!/bin/bash

set -e

source ../../platform/config/platform.env

source app.env

clear

echo "========================================"
echo " Tic Tac Toe - Deploy"
echo "========================================"

echo ""
echo "Application : $APP_NAME"
echo ""

#########################################
# Validate Files
#########################################

echo "[1/10] Checking project..."

FILES=(
    "app.py"
    "Dockerfile"
    "requirements.txt"
    "templates/index.html"
    "static/css/style.css"
    "static/js/game.js"
    "k8s/deployment.yaml"
    "k8s/service.yaml"
)

for file in "${FILES[@]}"
do

    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ Missing $file"
        exit 1
    fi

done

echo ""

#########################################
# Validate Platform
#########################################

echo ""
echo "[2/10] Validating Platform..."

if ! az account show >/dev/null 2>&1
then
    echo "❌ Azure is not logged in."
    exit 1
fi

if ! az acr show --name "$ACR_NAME" >/dev/null 2>&1
then
    echo "❌ Azure Container Registry not found."
    echo "Please start the platform first."
    exit 1
fi

if ! kubectl get nodes >/dev/null 2>&1
then
    echo "❌ AKS Cluster is not available."
    echo "Please start the platform first."
    exit 1
fi

echo "✓ Platform Ready"

#########################################
# Docker Build
#########################################

echo "[3/10] Building Docker image..."

echo ""

docker build \
    -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo ""

echo "✓ Docker image built successfully."

#########################################
# Login to Azure Container Registry
#########################################

echo ""

echo "[4/10] Logging into Azure Container Registry..."

az acr login --name $ACR_NAME

echo ""

echo "✓ Logged into Azure Container Registry."

echo ""

echo "[5/10] Tagging Docker Image..."

docker tag \
    ${IMAGE_NAME}:${IMAGE_TAG} \
    ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

echo ""

echo "✓ Image tagged."

echo ""

echo "[6/10] Pushing Image..."

docker push \
${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

echo ""

echo "✓ Image pushed successfully."

#########################################
# Prepare Kubernetes Manifest
#########################################

echo ""
echo "[7/10] Preparing Kubernetes Manifest..."

mkdir -p build

cp k8s/deployment.yaml build/deployment.yaml

sed -i "s|IMAGE_PLACEHOLDER|${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}|g" build/deployment.yaml

echo "✓ Kubernetes manifest generated."

#########################################
# Deploy Application
#########################################

echo ""
echo "[8/10] Deploying to AKS..."

kubectl apply -f build/deployment.yaml

kubectl apply -f k8s/service.yaml

echo "✓ Deployment submitted."

#########################################
# Wait for Rollout
#########################################

echo ""
echo "[9/10] Waiting for rollout..."

kubectl rollout status \
deployment/${DEPLOYMENT_NAME} \
--timeout=300s

echo ""

echo "Pods"

kubectl get pods -o wide

echo ""

echo "Services"

kubectl get svc


echo ""

echo "Waiting for External IP..."

EXTERNAL_IP=""

for i in {1..30}
do

    EXTERNAL_IP=$(kubectl get svc ${SERVICE_NAME} \
        -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

    if [ -n "$EXTERNAL_IP" ]; then
        echo "✓ External IP Assigned."
        break
    fi

    echo "Waiting... ($i/30)"

    sleep 10

done

echo ""

echo "========================================"

echo " Application Ready"

echo "========================================"

echo ""

echo "URL"

if [ -n "$EXTERNAL_IP" ]
then

    echo "http://${EXTERNAL_IP}"

else

    echo "LoadBalancer IP Pending"

fi

echo ""

#########################################
# Health Check
#########################################

echo ""
echo "[10/10] Health Check..."

kubectl get pods

kubectl get svc

echo ""

echo "========================================"
echo " Application Deployed"
echo "========================================"

echo ""

echo "Application : $APP_NAME"

echo "Namespace   : $NAMESPACE"

echo "Deployment  : $DEPLOYMENT_NAME"

echo "Service     : $SERVICE_NAME"

echo "Image       : ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"

echo ""

echo "✓ Deployment completed successfully."