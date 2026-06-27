#!/bin/bash

set -e
source scripts/lib/config.sh
source scripts/lib/common.sh

echo "========================================"
echo " Azure DevOps Demo - Startup Script"
echo "========================================"

echo ""
echo "[1/8] Checking Azure Login..."

if ! az account show >/dev/null 2>&1; then
    az login
fi

echo "Azure Login OK"

echo ""
echo "[2/8] Terraform Apply..."

cd terraform

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
echo "[3/8] Getting AKS Credentials..."

az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_NAME \
  --overwrite-existing

mkdir -p ~/.kube
cp /mnt/c/Users/Asus/.kube/config ~/.kube/config
chmod 600 ~/.kube/config

echo ""
echo "[4/8] Waiting for AKS Node..."

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

echo ""
echo "[6/8] Checking if image exists in ACR..."

info "Checking Docker image in ACR..."

if az acr repository show-tags \
    --name $ACR_NAME \
    --repository $IMAGE_NAME \
    --output tsv 2>/dev/null | grep -q "^${IMAGE_TAG}$"
then

    success "Docker image already exists in ACR."

else

    info "Docker image not found in ACR."

    if docker image inspect ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1
    then

        success "Local Docker image found."

    else

        info "Local Docker image missing."

        info "Building Docker image..."

        docker build \
            -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} \
            ./app

        success "Docker image built."

    fi

    info "Logging into Azure Container Registry..."

    az acr login --name $ACR_NAME

    info "Pushing image to ACR..."

    docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

    success "Docker image uploaded."
fi

info "Checking Helm release..."

if helm status $HELM_RELEASE >/dev/null 2>&1
then

    success "Helm release already exists."

    info "Upgrading release..."

    helm upgrade \
        $HELM_RELEASE \
        $HELM_CHART

else

    info "Installing Helm release..."

    helm install \
        $HELM_RELEASE \
        $HELM_CHART

fi

echo ""

info "Waiting for rollout..."

if kubectl rollout status deployment/$HELM_RELEASE --timeout=180s
then

    success "Deployment successful."

else

        echo ""
    info "Initial rollout failed."

    info "Checking AKS access to ACR..."

    if az aks check-acr \
        --resource-group "$RESOURCE_GROUP" \
        --name "$AKS_NAME" \
        --acr "${ACR_NAME}.azurecr.io" >/dev/null 2>&1
    then

        success "AKS can now pull images."

        info "Restarting deployment..."

        kubectl rollout restart deployment/$HELM_RELEASE

        info "Waiting for rollout again..."

        if kubectl rollout status deployment/$HELM_RELEASE --timeout=180s
        then

            success "Deployment recovered successfully."

        else

            echo ""
            error "Deployment failed after retry."

            echo ""
            info "Pods"

            kubectl get pods

            echo ""

            POD=$(kubectl get pods -o jsonpath='{.items[0].metadata.name}')

            info "Describe Pod"

            kubectl describe pod "$POD"

            echo ""

            info "Container Logs"

            kubectl logs "$POD" || true

            exit 1

        fi

    else

        error "AKS still cannot access ACR."

        exit 1

    fi
fi

echo ""
echo "========================================"
echo " Project Started Successfully!"
echo "========================================"

echo ""
echo "========================================"
echo " Platform Status"
echo "========================================"

NODE_COUNT=$(kubectl get nodes --no-headers | wc -l)

POD_STATUS=$(kubectl get pods --no-headers | grep Running | wc -l)

info "Waiting for LoadBalancer External IP..."

SERVICE_IP=""

for i in {1..30}
do

    SERVICE_IP=$(kubectl get svc ${HELM_RELEASE}-service \
        -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)

    if [ -n "$SERVICE_IP" ]
    then
        success "External IP assigned."
        break
    fi

    echo "Waiting... ($i/30)"
    sleep 10

done

if [ -z "$SERVICE_IP" ]
then
    error "Timed out waiting for LoadBalancer External IP."
fi

echo ""

echo "Azure Login       : OK"

echo "Terraform         : OK"

echo "AKS Nodes         : $NODE_COUNT"

echo "Running Pods      : $POD_STATUS"

echo "Helm Release      : $HELM_RELEASE"

echo "External IP       : ${SERVICE_IP:-Pending}"

echo ""

echo "Application URL"

if [ -n "$SERVICE_IP" ]; then
    echo "http://$SERVICE_IP:5000"
else
    echo "LoadBalancer IP is still pending."
fi

echo ""
echo "========================================"

success "Platform Ready!"
