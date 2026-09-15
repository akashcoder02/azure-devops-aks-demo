# Flask Demo Helm Chart

[Project guide](../docs/README.md)

This directory contains a separate Helm application chart. It is distinct from the two application paths used by the current release workflow.

## Contents

- Chart.yaml: chart name flask-demo, chart version 0.1.0, appVersion 1.16.0.
- values.yaml: image, replicas, service, and container-port defaults.
- templates/deployment.yaml: Deployment using configurable image and replica count.
- templates/service.yaml: Service using configurable port/type.
- templates/_helpers.tpl: naming and label helpers.

## Source defaults

| Setting | Value |
|---|---|
| Replicas | 2 |
| Image | agdevopsacr2026.azurecr.io/flask-demo:v1 |
| Container port | 5000 |
| Service port | 5000 |
| Service type | LoadBalancer |

Chart metadata appVersion is not proof of the Python application version or the deployed image's contents.

## Integration boundary

scripts/lib/config.sh references this chart and flask-demo image defaults. Current release.yml choices are tic-tac-toe and tetris, whose delivery uses their own manifests rather than this chart.

The chart does not supply the portal's GitHub environment configuration, local CLI tools, sibling repository files, or full operational runtime requirements. Installing it alone would not establish a fully functional portal.

Review the [portal packaging notes](../app/README.md) before treating the chart as a deployment package for app/.
