from scraper import Scraper
from utils import createListOfWebsites


def main() -> None:
    websites = createListOfWebsites()
    scraper = Scraper(websites)
    scraper.scrapeToFile("nmd")


if __name__ == "__main__":
    main()
