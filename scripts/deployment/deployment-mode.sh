#!/bin/bash

set -e

DEPLOYMENT_TYPE="$1"
APPLICATION_NAME="$2"

HPA_SOURCE="gitops/addons/hpa/${APPLICATION_NAME}.yaml"
HPA_DESTINATION="gitops/applications/${APPLICATION_NAME}/hpa.yaml"

echo "========================================="
echo "Deployment Mode Manager"
echo "========================================="

echo "Application      : ${APPLICATION_NAME}"
echo "Deployment Type  : ${DEPLOYMENT_TYPE}"

echo ""

case "$DEPLOYMENT_TYPE" in

default)

    echo "Default Deployment Selected"

    ;;

hpa)

    echo "HPA Deployment Selected"

    ;;

*)

    echo "ERROR"

    echo "Unknown Deployment Type"

    exit 1

    ;;

esac

if [ "$DEPLOYMENT_TYPE" = "hpa" ]; then

    if [ ! -f "$HPA_SOURCE" ]; then

        echo ""

        echo "HPA Manifest Missing"

        echo "$HPA_SOURCE"

        exit 1

    fi

    cp "$HPA_SOURCE" "$HPA_DESTINATION"

    echo ""

    echo "HPA Enabled"

else

    rm -f "$HPA_DESTINATION"

    echo ""

    echo "HPA Disabled"

fi

echo ""

echo "Deployment Mode Completed"

echo "========================================="
