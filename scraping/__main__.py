from dotenv import load_dotenv
from scraping.scraper import Scraper
from scraping.utils import createListOfWebsites
from app import create_app
import os
import argparse


load_dotenv()
WEBSITES = os.environ.get("WEBSITES_FILE")
ENV_TYPE = os.environ.get("ENV_TYPE")

# Initialize parser with arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-e",
    "--env_type",
    type=str,
    help="specify environment",
    default=ENV_TYPE,
)
parser.add_argument(
    "-d",
    "--delete_scraped",
    action="store_true",
    default=False,
    help="if set to True, all previously scraped products and product data will be removed from database in current environment",
)
parser.add_argument(
    "-w",
    "--websites",
    type=str,
    default=WEBSITES,
    help="path to json file containing info about websites to scrape",
)

parser.add_argument(
    "-f",
    "--to_file",
    action="store_true",
    default=False,
    help="if set to True scraped data will be stored to file scraped_data.json",
)

parser.add_argument(
    "-db",
    "--to_database",
    action="store_true",
    default=True,
    help="if set to True scraped data will be stored in environment database (default True)",
)


def main() -> None:
    args = parser.parse_args()
    env = args.env_type
    websites_config = args.websites
    app = create_app(env)
    websites = createListOfWebsites(websites_config)
    scraper = Scraper(websites, app)
    if args.to_file:
        scraper.scrapeToFile("scraped_data.json")
    if args.to_database and args.delete_scraped:
        scraper.scrapeToDb(delete_already_scraped=True)
    elif args.to_database:
        scraper.scrapeToDb()


if __name__ == "__main__":
    main()
