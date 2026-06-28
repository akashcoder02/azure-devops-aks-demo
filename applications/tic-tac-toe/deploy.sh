#!/bin/bash

set -e

clear

APP_NAME="tic-tac-toe"

IMAGE_NAME=$APP_NAME

IMAGE_TAG=latest

echo "========================================"
echo " Tic Tac Toe - Deploy"
echo "========================================"

echo ""
echo "Application : $APP_NAME"
echo ""

#########################################
# Validate Files
#########################################

echo "[1/6] Checking project..."

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
# Docker Build
#########################################

echo "[2/6] Building Docker image..."

echo ""

docker build \
    -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo ""

echo "✓ Docker image built successfully."

echo ""

echo ""

echo "========================================"
echo " Validation Successful"
echo "========================================"