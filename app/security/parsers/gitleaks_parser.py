from security.parsers.base_parser import (
    BaseParser
)

from security.scan_manager import (
    scan_manager
)


class GitleaksParser(BaseParser):

    def __init__(self):

        super().__init__(
            scan_manager.application_reports()
            / "secrets"
            / "gitleaks.json"
        )


gitleaks_parser = GitleaksParser()