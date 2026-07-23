SCANNERS = {

    "gitleaks": {
        "category": "application",
        "type": "Secrets",
        "report": "application/secrets/gitleaks.json"
    },

    "semgrep": {
        "category": "application",
        "type": "SAST",
        "report": "application/sast/semgrep.json"
    },

    "pip-audit": {
        "category": "application",
        "type": "Dependencies",
        "report": "application/dependencies/pip-audit.json"
    },

    "trivy": {
        "category": "application",
        "type": "Containers",
        "report": "application/containers/trivy.json"
    },

    "checkov": {
        "category": "platform",
        "type": "Terraform",
        "report": "platform/terraform/checkov.json"
    }

}