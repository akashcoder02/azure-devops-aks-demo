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

        return self.parser.parse()