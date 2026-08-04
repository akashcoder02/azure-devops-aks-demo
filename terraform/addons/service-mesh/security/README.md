# Service Mesh Security

## Overview

This module provisions Istio runtime security resources for applications deployed on the Azure DevOps Internal Developer Platform.

## Resources

- PeerAuthentication
- AuthorizationPolicy
- RequestAuthentication

## Features

- STRICT / PERMISSIVE / DISABLE mTLS
- Authorization Policies
- JWT Authentication
- Multi-application support
- Terraform managed
- Dashboard integration ready

## Variables

| Variable | Description |
|----------|-------------|
| mtls_mode | STRICT / PERMISSIVE / DISABLE |
| authorization_enabled | Enable AuthorizationPolicy |
| jwt_enabled | Enable RequestAuthentication |
| jwt_issuer | JWT Issuer |
| jwt_jwks_uri | JWKS Endpoint |

## Applications

The module automatically provisions security resources for every application defined in:

```
var.applications
```

Current applications:

- tic-tac-toe
- tetris

Future applications will automatically receive:

- PeerAuthentication
- AuthorizationPolicy
- RequestAuthentication

## Dashboard

This module is controlled from:

Service Mesh → Security

The dashboard will support:

- Enable STRICT mTLS
- Enable PERMISSIVE mTLS
- Disable mTLS
- Enable JWT
- Disable JWT
- Authorization Policies
