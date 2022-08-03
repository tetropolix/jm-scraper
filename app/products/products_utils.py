from scraping.schemas import (
    FilterOptions,
    createFilterOptions,
    createShoeSize,
)
from typing import Optional


def checkIfFilterShoudBeApplied(args: dict) -> bool:
    allowedFilterQueryParameters = [
        "brandName",
        "name",
        "minPrice",
        "maxPrice",
        "percentOff",
        "outOfStock",
        "shoeSize",
        "gender",
        "domain",
        "size_us",
        "size_uk",
        "size_eu",
        "size_cm",
    ]
    for param in allowedFilterQueryParameters:
        if args.get(param) != None:
            return True
    return False


def createFilterOptionsFromArgs(args) -> Optional[FilterOptions]:
    try:
        shoeSize = createShoeSize(
            {
                "us": args.getlist("size_us", type=str),
                "uk": args.getlist("size_uk", type=str),
                "eu": args.getlist("size_eu", type=str),
                "cm": args.getlist("size_cm", type=str),
            }
        )
        filterOptions = createFilterOptions(
            {
                "brandName": args.getlist("brandName", type=str) or None,
                "name": args.get("name", None, type=str),
                "minPrice": args.get("minPrice", None, type=float),
                "maxPrice": args.get("maxPrice", None, type=float),
                "percentOff": args.get("percentOff", None, type=float),
                "outOfStock": args.get(
                    "outOfStock",
                    None,
                    type=lambda val: val.lower() == "true"
                    if val.lower() in ["true", "false"]
                    else val,  # returning val as string proceeds to ValueError exception
                ),
                "shoeSize": shoeSize,
                "gender": [
                    gender.capitalize() for gender in args.getlist("gender", type=str)
                ]
                or None,
                "domain": args.getlist("domain", type=str) or None,
            }
        )
    except ValueError as e:
        return None
    return filterOptions if all([shoeSize, filterOptions]) else None
