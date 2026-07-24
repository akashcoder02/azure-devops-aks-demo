from security.scanner import Scanner

from security.parsers.gitleaks_parser import (
    gitleaks_parser
)

from security.parsers.semgrep_parser import (
    semgrep_parser
)

from security.parsers.trivy_parser import (
    trivy_parser
)

from security.parsers.pip_audit_parser import (
    pip_audit_parser
)

from security.parsers.checkov_parser import (
    checkov_parser
)

from security.parsers.aks_parser import (
    aks_parser
)

from security.parsers.helm_parser import (
    helm_parser
)

from security.parsers.dockerfile_parser import (
    dockerfile_parser
)

from security.parsers.workflow_parser import (
    workflow_parser
)

from security.config_loader import (
    config_loader
)

from security.parsers.kubernetes_parser import (
    kubernetes_parser
)



def get_application_scanners():

    config = config_loader.load()

    scanners = []

    if config["application"]["gitleaks"]:

        scanners.append(

            Scanner(
                name="Gitleaks",
                category="Secrets",
                parser=gitleaks_parser
            )

        )

    if config["application"]["semgrep"]:

        scanners.append(

            Scanner(
                name="Semgrep",
                category="SAST",
                parser=semgrep_parser
            )

        )

    if config["application"]["pip-audit"]:

        scanners.append(

            Scanner(
                name="Pip-Audit",
                category="Dependencies",
                parser=pip_audit_parser
            )

        )

    if config["application"]["trivy"]:

        scanners.append(

            Scanner(
                name="Trivy",
                category="Container",
                parser=trivy_parser
            )

        )

    if config["application"]["kubernetes"]:

        scanners.append(

            Scanner(
                name="Kubernetes",
                category="Kubernetes",
                parser=kubernetes_parser
            )

        )

    return scanners

def get_platform_scanners():

    config = config_loader.load()

    scanners = []

    if config["platform"]["checkov"]:

        scanners.append(

            Scanner(

                name="Checkov",

                category="Terraform",

                parser=checkov_parser

            )

        )

    if config["platform"]["aks"]:

        scanners.append(

            Scanner(

                name="AKS",

                category="Platform",

                parser=aks_parser

            )

        )

    if config["platform"]["helm"]:

        scanners.append(

            Scanner(

                name="Helm",

                category="Helm",

                parser=helm_parser

            )

        )

    if config["platform"]["dockerfiles"]:

        scanners.append(

            Scanner(

                name="Dockerfiles",

                category="Dockerfile",

                parser=dockerfile_parser

            )

        )

    if config["platform"]["workflows"]:

        scanners.append(

            Scanner(

                name="Workflows",

                category="GitHub Actions",

                parser=workflow_parser

            )

        )

    return scanners