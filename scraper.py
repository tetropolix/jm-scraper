from schemas import createFilterOptions
from website import Website
from typing import List
import json
from websiteParsers import getAllDataSVD
import time


class Scraper:
    def __init__(self, websitesToScrape: List[Website]):
        self.websitesToScrape = websitesToScrape

    def scrapeSite(
        self, website: Website
    ) -> List:  # TO DO IF ELSE LOGIC FOR OTHER SITES
        return getAllDataSVD(website)

    def scrape(self, filterKeywordsDict: dict) -> List:
        start = time.time()
        listOfScrapedData = []
        filterOptions = createFilterOptions(filterKeywordsDict)
        if filterOptions == None:
            print("Filter keywords passed in wrong format!")
            return None
        for website in self.websitesToScrape:
            scrapedData = self.scrapeSite(website)
            listOfScrapedData += scrapedData
        end = time.time()
        print(str(end - start) + " seconds")
        return listOfScrapedData

    def scrapeToFile(self, filterKeywordsDict: dict) -> None:
        scrapedData = self.scrape(filterKeywordsDict)
        with open("scrapedData" + ".json", "w") as file:
            file.write(json.dumps(scrapedData))
