import time
from scraping.schemas import ShoeProduct
from scraping.website import Website
from typing import List, Tuple
import json
import scraping
from database.scraping_db_actions import (
    getEshopsDict,
    insertProduct,
    insertProductData,
    remove_products_with_product_data,
)
from datetime import datetime


class AppInstanceError(Exception):
    pass


class Scraper:
    def __init__(self, websitesToScrape: List[Website], appInstance):
        if not appInstance:
            raise AppInstanceError("App instance cannot be None")
        self.websitesToScrape = websitesToScrape
        self.appInstance = appInstance

    def scrapeSite(self, website: Website) -> List[ShoeProduct]:
        try:
            scrapeFn = getattr(scraping, website.scrapeFunctionName)
            return scrapeFn(website)
        except AttributeError as e:
            print("Scrape function for {} was not found!".format(website.domain))
            print(str(e))
            return []

    def scrape(self) -> List[ShoeProduct]:
        start = time.time()
        listOfScrapedData = []
        for website in self.websitesToScrape:
            scrapedData = self.scrapeSite(website)
            listOfScrapedData += scrapedData
        end = time.time()
        print(str(end - start) + " seconds")
        return listOfScrapedData

    def scrapeToFile(self, filePath: str) -> None:
        scrapedData = self.scrape()
        scrapedData = [product.toDict() for product in scrapedData]
        with open(filePath, "w") as file:
            file.write(json.dumps(scrapedData))

    def scrapeToDb(self) -> None:
        scrapedData = self.scrape()
        scrapedAt = datetime.now()
        productDataInserted = 0
        start = time.time()
        with self.appInstance.app_context():
            eshops = getEshopsDict()
            for product in scrapedData:
                productId = insertProduct(product)
                productDataId = insertProductData(productId, product, scrapedAt, eshops)
                if productDataId != None:
                    productDataInserted += 1
        end = time.time()
        print(
            str(end - start)
            + " seconds for records insertion - %d records inserted"
            % productDataInserted
        )

    def removeAlreadyScraped(self) -> Tuple[int, int]:
        with self.appInstance.app_context():
            removed = remove_products_with_product_data()
        print("Removed products -", removed[0])
        print("Removed product data -", removed[1])
