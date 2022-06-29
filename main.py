from scraper import Scraper
from utils import createListOfWebsites


def main() -> None:
    filterKeywords = {
        "name": "vans",
        "brandName": "adidas Consortium",
        "finalPrice": 360,
        "shoeSize": 12.5,
    }
    websites = createListOfWebsites()
    scraper = Scraper(websites)
    scraper.scrapeToFile(filterKeywords)


if __name__ == "__main__":
    main()
