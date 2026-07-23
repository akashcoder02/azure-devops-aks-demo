from security.history_manager import (
    history_manager
)


class Scanner:

    def __init__(
        self,
        name,
        category,
        parser,
        enabled=True
    ):

        self.name = name
        self.category = category
        self.parser = parser
        self.enabled = enabled

    def run(self):

        result = self.parser.parse()

        history_manager.add(

            scanner=self.name,

            category=self.category,

            status=result.get(
                "status",
                "Unknown"
            ),

            findings=result.get(
                "findings",
                0
            ),

            critical=result.get(
                "critical",
                0
            )

        )

        return result