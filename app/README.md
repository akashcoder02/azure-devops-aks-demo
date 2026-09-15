# Developer Portal

[Project guide](../docs/README.md) · [Architecture](../docs/architecture/README.md)

## Implementation

The entry point is [app.py](app.py). It loads environment configuration, creates Flask, and registers blueprints. Direct execution starts the Flask development server on port 5000 with debug enabled.

| Directory | Responsibility |
|---|---|
| routes/ | Page and API handlers |
| services/ | GitHub, Azure, Kubernetes, jobs, and dashboard integration |
| templates/ | Jinja pages and partials |
| static/ | JavaScript behavior and CSS |
| config/ | GitHub environment loading and DevSecOps settings |
| security/ | Stored-report parsing and policy evaluation |

There is no separate frontend build pipeline. Browser JavaScript calls Flask APIs and updates server-rendered pages.

## Functional areas

- Dashboard and infrastructure status.
- Sample application release and undeployment.
- Platform provisioning, destruction, and diagnostics.
- Add-on installation and status.
- Argo CD visibility, HPA, resource inventory, and deployment history.
- DevSecOps reports, policies, scores, and trends.
- Istio overview, traffic, security, and resilience controls.

Representative read endpoints include /health, /api/dashboard, /api/resources, /api/hpa, and /api/service-mesh/overview. POST /api/run can start local lifecycle scripts. Page names and HTTP methods alone should not be used to infer absence of side effects: reading some security pages records local history.

## Execution paths

[services/github.py](services/github.py) dispatches GitHub workflows. Other GitHub service classes handle release actions and status. A successful dispatch response means GitHub accepted the request; it does not mean deployment completed.

Local status services invoke az and kubectl using the host's current contexts. The dashboard caches results for approximately ten seconds. Local job managers run Bash in background threads and share an in-memory job record. The script runner uses script-specific working directories.

## Runtime configuration

| Setting | Purpose |
|---|---|
| GITHUB_OWNER | Repository owner |
| GITHUB_REPOSITORY | Repository name |
| GITHUB_PAT | Credential for the GitHub API calls the portal performs |
| RELEASE_WORKFLOW | Optional override; default release.yml |
| platform/config/platform.env | Resource names used by the newer dashboard |
| config/devsecops.json | Scanner selection and policy settings |

Credentials are runtime inputs; never paste working credentials into documentation or committed configuration.

The portal host requires Python and [requirements.txt](requirements.txt). Operational features additionally require suitable Azure CLI, kubectl, and, for local lifecycle scripts, Terraform, Bash and relevant shell utilities. Release building in GitHub Actions uses the runner's Docker installation, not the browser.

From the repository root, the application entry command is:

```bash
python app/app.py
```

This assumes dependencies and intended runtime configuration are already available. It launches an interactive control surface; it does not provision the platform merely by starting. The development server is not a production serving configuration.

## Packaging boundaries

[Dockerfile](Dockerfile) installs Python requirements, copies app content, and starts app.py. It does not install az, kubectl, or Terraform. A build using app/ as context also excludes sibling scripts/, platform/, reports/, and history/ expected by several services. Therefore the Dockerfile alone is not a complete deployment package for every portal feature.

## Known implementation gaps

- Portal authentication, per-user roles, and server-side approval controls are not implemented in the inspected wiring.
- Local jobs and deployment context are process-local, not a durable queue.
- The GitHub status service fetches the latest repository workflow run rather than a stored exact run ID for each request.
- ApplicationsService contains fixed catalog values, including some pod/HPA/deployment labels; distinguish those from the newer dashboard's live queries.
- The VM provisioning route references scripts/create-vm.sh, which is absent.
- Empty routes, templates, and styles are scaffolding; file presence does not mean a feature is active.
- CLI errors can appear as unavailable resources; missing tools, credentials, or context should be checked before assuming infrastructure is absent.

See [security implementation](security/README.md) for report-side effects and enforcement boundaries.
