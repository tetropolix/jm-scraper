from string import Template
from typing import List, Dict
from schemas import FilterOptions, createFilterOptions


class Website:
    def __init__(
        self,
        customName: str,
        domain: str,
        queryUrl: str,
        queryUrlWithFilters: str,
        filterOptionsForManualRequest: Dict[str, str],
    ):
        self.customName = customName
        self.domain = domain
        self.queryUrl = queryUrl
        self.queryUrlWithFilters = queryUrlWithFilters
        self.filterOptionsForManualRequest = filterOptionsForManualRequest

    """ def prepareFilterUrl(
        self,
        filterOptions: FilterOptions,
        parseFilterOptionsForSpecificSite: Callable[[FilterOptions], dict],
    ) -> str:
        t = Template(self.urlForFilterSearch)
        filterOptionsWithoutConstraintsDict = {}
        for key, value in dict(filterOptions).items():
            if key in self.filterKeywordConstrains:
                continue
            filterOptionsWithoutConstraintsDict[key] = value
        filterOptionsWithoutConstraints = createFilterOptions(
            filterOptionsWithoutConstraintsDict
        )
        finalFilterOptions = parseFilterOptionsForSpecificSite(
            filterOptionsWithoutConstraints
        )
        print(finalFilterOptions)
        return t.safe_substitute(**finalFilterOptions) """
