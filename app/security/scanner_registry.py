from security.scanner import Scanner

from security.parsers.gitleaks_parser import gitleaks_parser
from security.parsers.semgrep_parser import semgrep_parser

from security.config_loader import config_loader

from security.parsers.checkov_parser import (
    checkov_parser
)

from security.parsers.aks_parser import (
    aks_parser
)
from security.parsers.trivy_parser import (
    trivy_parser
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

    if config["application"]["trivy"]:

        scanners.append(

            Scanner(

                name="Trivy",

                category="Container",

                parser=trivy_parser

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

    return scanners