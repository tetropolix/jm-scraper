import time
from scraping.schemas import ShoeProduct
from scraping.website import Website
from typing import List, Tuple
import json
import scraping
from database.scraping_db_actions import (
    get_products_count,
    getEshopsDict,
    insert_data_about_scrape,
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
        self.last_scraping_time = 0

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
        self.last_scraping_time = end - start
        print(str(self.last_scraping_time) + " seconds")
        return listOfScrapedData

    def scrapeToFile(self, filePath: str) -> None:
        scrapedData = self.scrape()
        scrapedData = [product.toDict() for product in scrapedData]
        with open(filePath, "w") as file:
            file.write(json.dumps(scrapedData))

    def scrapeToDb(self, delete_already_scraped=False) -> None:
        scraped_data = self.scrape()
        scraped_at = datetime.now()
        product_data_inserted = 0
        products_inserted = 0
        start = time.time()

        with self.appInstance.app_context():
            if delete_already_scraped:
                removed = remove_products_with_product_data()
                print("Removed products -", removed[0])
                print("Removed product data -", removed[1])
            eshops = getEshopsDict()
            for product in scraped_data:
                product_id, newly_inserted = insertProduct(product)
                if newly_inserted:
                    products_inserted += 1
                product_data_id = insertProductData(
                    product_id, product, scraped_at, eshops
                )
                if product_data_id != None:
                    product_data_inserted += 1
            insertion_time = time.time() - start
            products_count = get_products_count()
            insert_data_about_scrape(
                scraped_at,
                products_inserted,
                product_data_inserted,
                self.last_scraping_time,
                products_count,
            )
        print(
            str(insertion_time)
            + " seconds for records insertion - %d product data records inserted and %d new products"
            % (product_data_inserted, products_inserted)
        )
