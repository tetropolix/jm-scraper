from schemas import createShoeProduct
from website import Website
from typing import List
import requests, json
from string import Template


def makeRequest(url: str, domain: str) -> dict:
    try:
        r = requests.get(url)
        return json.loads(r.content)
    except requests.exceptions.RequestException:
        print("Failed to request " + domain)
        return None


def parseDataSVD(website: Website, filterKeyword: str) -> List:
    obtainedProducts = []
    output = []
    url = website.prepareFilterUrl(filterKeyword)
    t = Template(url)
    currentPage = 1
    while currentPage < 20:  # TO DO: MAX REQUEST THRESHOLD
        url = t.safe_substitute(currentPageValue=str(currentPage))
        data = makeRequest(url, filterKeyword)
        if data == None or len(data["data"]["products"]["items"]) == 0:
            break
        else:
            obtainedProducts += data["data"]["products"]["items"]
        currentPage += 1
    for product in obtainedProducts:
        productData = {}
        productData["brandName"] = product["brand_name"]
        productData["name"] = product["name"]
        productData["sku"] = product["sku"]
        productData["smallImageUrl"] = product["small_image"]["url"]
        productData["url"] = product["url"]
        productData["finalPrice"] = product["final_price"]
        productData["originalPrice"] = product["original_price"]
        productData["percentOff"] = product["percent_off"]
        productData["outOfStock"] = product["state"] != None
        productData["domain"] = website.domain
        shoeProduct = createShoeProduct(productData)
        if shoeProduct != None:
            output.append(productData)
    return output


class Scraper:
    def __init__(self, websitesToScrape: List[Website]):
        self.websitesToScrape = websitesToScrape

    def scrape_site(
        self, website: Website, filterKeyword: str
    ) -> List:  # TO DO IF ELSE LOGIC FOR OTHER SITES
        return parseDataSVD(website, filterKeyword)

    def scrape(self, filterKeyword) -> List:
        listOfScrapedData = []
        for website in self.websitesToScrape:
            scrapedData = self.scrape_site(website, filterKeyword)
            listOfScrapedData += scrapedData
        return listOfScrapedData

    def scrapeToFile(self, filterKeyword) -> None:
        scrapedData = self.scrape(filterKeyword)
        with open("scrapedData" + ".json", "w") as file:
            file.write(json.dumps(scrapedData))
