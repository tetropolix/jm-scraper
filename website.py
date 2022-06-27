from string import Template

class Website:
    def __init__(self, customName, domain, urlForFilterSearch):
        self.customName: str = customName
        self.domain: str = domain
        self.urlForFilterSearch: str = urlForFilterSearch

    def prepareFilterUrl(self, filterKeyword: str) -> str:
        t = Template(self.urlForFilterSearch)
        return t.safe_substitute(filterKeyword=filterKeyword)
