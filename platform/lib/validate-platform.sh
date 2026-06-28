#!/bin/bash

validate_platform(){

    echo ""
    echo "========== Platform Validation =========="
    echo ""

    #########################################
    # Azure Login
    #########################################

    if az account show >/dev/null 2>&1
    then
        echo "✅ Azure Login"
    else
        echo "❌ Azure Login"
        return 1
    fi

    #########################################
    # Docker
    #########################################

    if docker info >/dev/null 2>&1
    then
        echo "✅ Docker Running"
    else
        echo "❌ Docker Not Running"
        return 1
    fi

    #########################################
    # Kubectl
    #########################################

    if kubectl version --client >/dev/null 2>&1
    then
        echo "✅ kubectl"
    else
        echo "❌ kubectl Missing"
        return 1
    fi

    #########################################
    # Terraform
    #########################################

    if terraform version >/dev/null 2>&1
    then
        echo "✅ Terraform"
    else
        echo "❌ Terraform Missing"
        return 1
    fi

    echo ""
}
