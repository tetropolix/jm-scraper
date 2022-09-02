class Website:
    def __init__(
        self,
        customName: str,
        domain: str,
        config: dict,
        scrapeFunctionName: str,
    ):
        self.customName = customName
        self.domain = domain
        self.config = config
        self.scrapeFunctionName = scrapeFunctionName
