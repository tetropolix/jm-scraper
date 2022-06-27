from typing import List
from website import Website
import json


def createListOfWebsites() -> List[Website]:
    websiteList = []
    with open("./websites.json", "r") as file:
        content = file.read()
        contentDict = json.loads(content)
    for record in contentDict.values():
        websiteList.append(
            Website(
                record["customName"], record["domain"], record["urlForFilterSearch"]
            )
        )
    return websiteList
