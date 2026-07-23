from security.scanner import Scanner

from security.parsers.gitleaks_parser import (
    gitleaks_parser
)


APPLICATION_SCANNERS = [

    Scanner(
        name="Gitleaks",
        category="Secrets",
        parser=gitleaks_parser
    )

]


PLATFORM_SCANNERS = [

]