from time import time
from typing import Any, List, Optional, Union
from scraping.website import Website
import json
import requests
import random
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

REQUEST_TIMEOUT = 0.05  # in seconds


def getRandomUserAgent() -> str:
    return random.choice(
        [
            "Opera/8.67 (Windows NT 5.2; sl-SI) Presto/2.12.297 Version/10.00",
            "Mozilla/5.0 (Windows CE) AppleWebKit/5310 (KHTML, like Gecko) Chrome/38.0.805.0 Mobile Safari/5310",
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/5342 (KHTML, like Gecko) Chrome/40.0.822.0 Mobile Safari/5342",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_7) AppleWebKit/5320 (KHTML, like Gecko) Chrome/36.0.869.0 Mobile Safari/5320",
            "Opera/8.39 (X11; Linux i686; sl-SI) Presto/2.10.353 Version/10.00",
            "Opera/9.26 (X11; Linux x86_64; sl-SI) Presto/2.9.243 Version/10.00",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_1 rv:6.0; en-US) AppleWebKit/534.7.3 (KHTML, like Gecko) Version/5.0.5 Safari/534.7.3",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X; en-US) AppleWebKit/533.29.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B111 Safari/6533.29.4",
            "Opera/8.88 (Windows NT 5.0; sl-SI) Presto/2.11.194 Version/11.00",
            "Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20130525 Firefox/35.0",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/5361 (KHTML, like Gecko) Chrome/40.0.814.0 Mobile Safari/5361",
            "Mozilla/5.0 (X11; Linux x86_64; rv:6.0) Gecko/20110911 Firefox/36.0",
            "Opera/8.12 (X11; Linux x86_64; en-US) Presto/2.12.299 Version/10.00",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_9 rv:4.0; sl-SI) AppleWebKit/532.5.3 (KHTML, like Gecko) Version/4.0 Safari/532.5.3",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_4 rv:6.0; en-US) AppleWebKit/532.30.2 (KHTML, like Gecko) Version/5.0 Safari/532.30.2",
            "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 4.0; Trident/3.0)",
            "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_6_6) AppleWebKit/5312 (KHTML, like Gecko) Chrome/39.0.830.0 Mobile Safari/5312",
            "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_7_7 rv:5.0; en-US) AppleWebKit/533.17.7 (KHTML, like Gecko) Version/4.0.5 Safari/533.17.7",
            "Mozilla/5.0 (Windows; U; Windows 98; Win 9x 4.90) AppleWebKit/531.20.2 (KHTML, like Gecko) Version/4.0.4 Safari/531.20.2",
            "Mozilla/5.0 (Windows NT 5.0; sl-SI; rv:1.9.2.20) Gecko/20170328 Firefox/35.0",
        ]
    )


def createListOfWebsites(websitesJsonPath: str) -> List[Website]:
    websiteList = []
    with open(websitesJsonPath, "r") as file:
        content = file.read()
        contentDict = json.loads(content)
    for record in contentDict.values():
        websiteList.append(
            Website(
                record["customName"],
                record["domain"],
                record["config"],
                record["scrapeFunctionName"],
            )
        )
    return websiteList


def makeRequest(url: str, headers: dict = None, wait: bool = True) -> Optional[dict]:
    if wait:
        time.sleep(REQUEST_TIMEOUT)
    if not headers:
        headers = {"User-Agent": getRandomUserAgent()}
    else:
        headers["User-Agent"] = getRandomUserAgent()
    try:
        r = requests.get(url, headers=headers)
        print(r.headers)
        print(r.cookies)
        print(r.content)
        if r.status_code > 299 or r.status_code < 200:
            print("Failed to request " + url + " - Status code " + str(r.status_code))
        elif r == None:
            print("{} returned None!".format(url))
        else:
            return r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        print("Failed to request " + url + " " + str(e))
    return None


def make_request(
    url: str, headers: dict = None, wait: bool = True
) -> Optional[requests.Response]:
    if wait:
        time.sleep(REQUEST_TIMEOUT)
    if not headers:
        headers = {"User-Agent": getRandomUserAgent()}
    else:
        headers["User-Agent"] = getRandomUserAgent()
    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Failed to request " + url + " " + str(e))
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


def sizeIsRange(val: str) -> bool:
    return "-" in val
