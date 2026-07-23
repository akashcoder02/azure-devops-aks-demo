from security.parsers.base_parser import (
    BaseParser
)

from security.scan_manager import (
    scan_manager
)


class SemgrepParser(BaseParser):

    def __init__(self):

        super().__init__(
            scan_manager.application_reports()
            / "sast"
            / "semgrep.json"
        )


semgrep_parser = SemgrepParser()