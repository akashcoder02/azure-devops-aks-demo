# {{ values.appName }}

{{ values.description }}

Generated through the Azure IDP Backstage Golden Path.

## Architecture

- Flask application and REST API
- MySQL database
- Kubernetes Deployment and Service
- PersistentVolumeClaim for MySQL data
- Azure Key Vault integration for database credentials
- ArgoCD GitOps configuration

## Environment

{{ values.environment }}

## Requested database storage

{{ values.storageSize }}

## Endpoints

- `/` — bucket-list user interface
- `/api/items` — list and add items
- `/health` — application and database health
