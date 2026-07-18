# Logging Addon

## Components

- Loki
- Fluent Bit

## Purpose

Provides centralized logging for AKS.

## Installed Resources

- Namespace
- Loki
- Fluent Bit

## Verification

kubectl get pods -n logging

kubectl get daemonsets -n logging

kubectl logs ...

## Grafana

Explore

↓

Loki