#!/bin/bash

set -e

#########################################
# Docker Module
# Azure DevOps Platform
#########################################

source scripts/lib/config.sh
source scripts/lib/common.sh

#########################################
# Check Docker Installation
#########################################

check_docker() {

    info "Checking Docker installation..."

    if command -v docker >/dev/null 2>&1
    then
        success "Docker is installed."
    else
        error "Docker is not installed."
    fi
}

#########################################
# Check Docker Daemon
#########################################

check_docker_daemon() {

    info "Checking Docker daemon..."

    if docker info >/dev/null 2>&1
    then
        success "Docker daemon is running."
    else
        error "Docker daemon is not running. Please start Docker Desktop."
    fi
}

#########################################
# Check Azure Container Registry
#########################################

check_acr() {

    info "Checking Azure Container Registry..."

    if az acr show --name "$ACR_NAME" >/dev/null 2>&1
    then
        success "Azure Container Registry exists."
    else
        error "Azure Container Registry does not exist."
    fi
}

#########################################
# Login to ACR
#########################################

login_acr() {

    info "Logging into Azure Container Registry..."

    az acr login --name "$ACR_NAME" >/dev/null

    success "Logged into ACR."
}

#########################################
# Check Local Docker Image
#########################################

check_local_image() {

    if docker image inspect ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1
    then

        success "Local Docker image found."

    else

        info "Local Docker image not found."

        build_image

    fi
}

#########################################
# Build Docker Image
#########################################

build_image() {

    info "Building Docker image..."

    docker build \
        -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} \
        ./app

    success "Docker image built."
}

#########################################
# Check Remote Image
#########################################

check_remote_image() {

    info "Checking Docker image in ACR..."

	TAGS=$(az acr repository show-tags \
    --name "$ACR_NAME" \
    --repository "$IMAGE_NAME" \
    --output tsv | tr -d '\r')

if echo "$TAGS" | grep -Fxq "$IMAGE_TAG"
    then

        success "Docker image already exists in ACR."

        return 0

    else

        info "Docker image not found in ACR."

        return 1

    fi
}

#########################################
# Push Docker Image
#########################################

push_image() {

    info "Pushing Docker image..."

    docker push \
        ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}

    success "Docker image pushed."
}

#########################################
# Verify Push
#########################################

verify_push() {

    info "Verifying image upload..."

    TAGS=$(az acr repository show-tags \
    --name "$ACR_NAME" \
    --repository "$IMAGE_NAME" \
    --output tsv | tr -d '\r')

    echo "===== DEBUG ====="
    echo "$TAGS"
    echo "================="

    if echo "$TAGS" | grep -Fxq "$IMAGE_TAG"
    then
        success "Image verified in Azure Container Registry."
    else
        error "Image upload verification failed."
        return 1
    fi
}

#########################################
# Main Flow
#########################################

check_docker

check_docker_daemon

check_acr

login_acr

check_local_image

if check_remote_image
then

    success "Skipping Docker push."

else

    push_image

    verify_push

fi

success "Docker module completed successfully."
