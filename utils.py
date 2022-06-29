from typing import Any, List, Optional, Union
from website import Website
import json
import requests


def createListOfWebsites() -> List[Website]:
    websiteList = []
    with open("./websites.json", "r") as file:
        content = file.read()
        contentDict = json.loads(content)
    for record in contentDict.values():
        websiteList.append(
            Website(
                record["customName"],
                record["domain"],
                record["queryUrl"],
                record["queryUrlWithFilters"],
                record["filterOptionsForManualRequest"],
            )
        )
    return websiteList


def makeRequest(url: str, domain: str) -> dict:
    try:
        r = requests.get(url)
        if r.status_code > 299 or r.status_code < 200:
            print(
                "Failed to request " + domain + " - Status code " + str(r.status_code)
            )
        else:
            return json.loads(r.content)
    except requests.exceptions.RequestException as e:
        print("Failed to request " + domain + " " + str(e))
    return None


def tryToFloatConversion(val: Any) -> Optional[float]:
    try:
        return float(val)
    except ValueError:
        return None


def floatOrIntFromStr(val: str) -> Union[float, int]:
    f = float(val)
    if int(f) == f:
        return int(f)
    else:
        return f
