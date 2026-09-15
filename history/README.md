# Deployment History

[Project guide](../docs/README.md)

[deployment-history.csv](deployment-history.csv) stores deployment records committed to the repository.

## Record schema

| Field | Intended content |
|---|---|
| Timestamp | Operation time |
| Application | Application name |
| Operation | Operation label |
| Image | Selected/running image |
| PreviousImage | Previous image or placeholder |
| Replicas | Recorded replica count |
| GitCommit | Associated commit |
| Workflow | Workflow name |
| GitHubUser | Actor |
| Status | Recorded result |
| Remarks | Additional description |

## Producers and consumers

The GitOps deployment workflow appends a successful release record and attempts to commit/push the file. Those history steps use continue-on-error, so deployment success does not guarantee history was saved.

The newer platform dashboard reads the local CSV. The separate deployment-history service retrieves repository history over HTTP. These consumers can show different freshness depending on the portal's local checkout.

## Limitations

This file is an operational convenience, not a complete audit trail. It does not capture every direct cluster change, failure, or workflow. Concurrent Git writers can conflict. CSV values are emitted by shell code rather than a durable event service.

Use exact workflow runs, Git commits, desired manifests, and runtime checks together when reconstructing a release. Do not use this CSV alone to assert that a particular version is currently running.
