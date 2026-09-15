# Stored Security Reports

[Project guide](../docs/README.md) · [Security implementation](../app/security/README.md)

reports/security contains generated scanner output consumed by portal parsers. A committed report is historical evidence with a particular scope and timestamp; it is not current proof of cluster or release security.

## Layout

| Path under security/ | Content |
|---|---|
| application/secrets | Gitleaks output |
| application/sast | Semgrep output |
| application/dependencies | pip-audit output |
| application/trivy | Trivy filesystem output |
| application/kubernetes | Merged Kubernetes findings |
| platform/terraform | Checkov output |
| platform/aks | AKS summary |
| platform/helm | JSON summary and text output |
| platform/dockerfiles | JSON summary and Hadolint text output |
| platform/workflows | JSON summary and Actionlint text output |

Other empty root-level report files and alternate folders exist. The paths selected in app/security/parsers are the authoritative inputs for the newer dashboard; not every similarly named file is consumed.

## Producers and consumers

The consolidated security-scan workflow normalizes report timestamps, commits output, and uploads a devsecops-security-reports artifact with a configured 30-day retention. Standalone scanner workflows upload separate artifacts and should not be assumed to populate the same portal inputs.

Portal parsers run against local files. Pulling newer repository content or designing artifact ingestion is necessary to refresh those inputs; the current implementation does not establish automatic artifact synchronization.

## Interpret results carefully

Some stored data predates the inspected code snapshot. The consolidated AKS JSON is generated from fixed labels. Some lint summaries contain empty findings despite separate diagnostic text. A Completed label or empty list alone is insufficient evidence of a clean scan.

For an assessment, identify the source commit, scanner version, scan scope, run status, raw output, and timestamp. See the security guide for the release-gate freshness gap.

## History

The workflow can create security/history/history.json. The portal also appends to that path when parsing results, so it mixes execution summaries and view-driven entries rather than representing a single immutable scan history.

The DevSecOps Terraform add-on creates storage containers, but repository/artifact reports are the implemented data path. No automatic upload into those containers is established by the inspected workflow.
