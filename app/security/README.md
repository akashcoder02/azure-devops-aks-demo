# Security Reports and Policy Implementation

[Project guide](../../docs/README.md) · [Stored reports](../../reports/README.md)

## Architecture

The portal reads scanner reports produced elsewhere. Scanner.run() calls a parser and records a history entry; despite the method name, it does not invoke the external scanning tool.

| Component | Role |
|---|---|
| config_loader.py | Load app/config/devsecops.json |
| scanner_registry.py | Select enabled application/platform scanners |
| parsers/ | Convert stored JSON into dashboard fields |
| orchestrator.py | Aggregate application/platform results |
| policies/policy_engine.py | Evaluate critical/high finding counts |
| scoring/security_score.py | Compute dashboard score and grade |
| history_manager.py | Append local JSON history |
| scan_manager.py | Resolve repository report paths |

## Scanner categories

| Category | Tool/path |
|---|---|
| Secrets | Gitleaks |
| Static analysis | Semgrep |
| Python dependencies | pip-audit |
| Filesystem vulnerabilities | Trivy; consolidated workflow uses trivy fs |
| Kubernetes manifests | Kubesec and report merger |
| Terraform | Checkov |
| AKS | Consolidated generated summary; separate workflow queries AKS |
| Helm | Helm lint |
| Dockerfiles | Hadolint |
| GitHub workflows | Actionlint |

Trivy's category label in the portal should not be interpreted as proof that the exact released container image was scanned.

## Data flow

The consolidated security-scan workflow writes reports under reports/security, attempts to commit them to Git, and uploads an Actions artifact. Portal parsers consume local copies of repository files. There is no implemented automatic portal refresh from each newly completed artifact.

Reading security views can append reports/security/history/history.json through Scanner.run(). They are not strictly side-effect-free report reads.

## Policy behavior

Current settings enable the listed scanners and configure mode=audit, block_on_critical=true, and high_threshold=10.

The policy engine sets blocked for critical findings when configured. Exceeding the high threshold appends a reason but does not set blocked. The mode value is reported but is not used to disable critical blocking. Therefore the audit label does not fully describe enforcement.

The release workflow invokes policy_engine.py and uses its exit status as a gate. However, it checks out the triggering revision and does not explicitly download fresh scan artifacts into the gate job. Reports committed by the scan job are not guaranteed to be the reports evaluated for that release.

## Evidence limitations

- The consolidated AKS report contains generated fixed status fields, not a live policy assessment.
- Helm lint references helm/tic-tac-toe, absent from the inspected tree; the existing chart is flask-demo.
- Hadolint references a root Dockerfile, absent from the inspected tree; actual Dockerfiles are under app/ and applications/.
- Helm, Dockerfile, and workflow JSON summaries are written with empty findings even when separate text output contains errors.
- Several scanner commands tolerate nonzero exits; execution failure and clean results need distinct handling.
- History generation in the workflow overwrites a summary file; portal reads append their own records. Neither is a complete immutable scan ledger.
- Missing, stale, empty, or unparsable reports must not be interpreted as verified security.

These limitations are documentation of existing behavior, not fixes.

## Runtime security is separate

Key Vault/managed identity and Istio policies are implemented through infrastructure and workflows, not these parsers. See [add-ons](../../terraform/addons/README.md).

Portal user authentication and authorization are another distinct concern; they are not supplied by a security score, GitHub repository permissions, or workload mTLS.

Before using this as a release control, establish report provenance for the exact commit/image, preserve scanner failures, validate policy behavior with representative results, and verify the runtime policies independently.
