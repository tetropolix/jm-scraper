from scraping.website import Website
from scraping.schemas import ShoeProduct, createShoeProduct, createShoeSize
from typing import Dict, List, Optional, Union
from scraping.utils import makeRequest, sizeIsRange
import urllib.parse
from string import Template
from scraping.schemas import createShoeProduct
from operator import itemgetter
from . import MAX_REQUESTS

# utils


def createShoeProductList(productsDict: dict) -> List[ShoeProduct]:
    shoeProductList = []
    for product in productsDict.values():
        shoeSize = createShoeSize(product["shoeSize"])
        if shoeSize == None:
            continue
        product["shoeSize"] = shoeSize
        shoeProductList.append(createShoeProduct(product))
    return list(filter(None, shoeProductList))


####


def createFilterUrlPartSVD(filterKeyword: str, value: str) -> str:
    toEncode = f'"{filterKeyword}":{{"eq":"{value}"}}'
    toEncode = toEncode + ","
    return urllib.parse.quote(toEncode)


def parseInitiallyObtainedDataSVD(
    data: List[dict], website: Website
) -> Dict[str, dict]:
    smallImageUrlPrefix = itemgetter("smallImageUrlPrefix")(website.config)
    output = {}
    for product in data:
        eshopId = str(product["id"])
        productData = {}
        productData["brandName"] = product["brand_name"]
        productData["name"] = product["name"]
        productData["shoeId"] = product["sku"]
        productData["smallImageUrl"] = (
            smallImageUrlPrefix + product["small_image"]["url"]
        )
        productData["url"] = product["url"]
        productData["finalPrice"] = product["final_price"]
        productData["originalPrice"] = product["original_price"]
        productData["percentOff"] = product["percent_off"]
        productData["outOfStock"] = product["state"] != None
        productData["shoeSize"] = {"us": set()}
        productData["gender"] = set()
        productData["eshopId"] = eshopId
        productData["domain"] = website.domain

        output[eshopId] = productData
    return output


def getProductsSVD(website: Website, filterUrlPart: str = None) -> List:
    obtainedProducts = []
    queryUrl, queryUrlWithFilters, headers = itemgetter(
        "queryUrl", "queryUrlWithFilters", "headers"
    )(website.config)
    url = queryUrl if filterUrlPart == None else queryUrlWithFilters
    t = Template(url)
    if filterUrlPart != None:
        url = t.safe_substitute(FILTEROPTION=filterUrlPart)
        t = Template(url)
    currentPage = 1
    while currentPage < MAX_REQUESTS:  # TO DO: MAX REQUEST THRESHOLD
        print(
            "Making request number {num} from {domain} - filterUrlPart = {filterUrlPart}".format(
                num=currentPage, domain=website.domain, filterUrlPart=filterUrlPart
            )
        )
        url = t.safe_substitute(currentPageValue=str(currentPage))
        data = makeRequest(url, headers=headers)
        try:
            if data == None or len(data["data"]["products"]["items"]) == 0:
                break
            else:
                obtainedProducts += data["data"]["products"]["items"]
        except KeyError as e:
            print("Structure for products in {} has changed!".format(website.domain))
            print(str(e))
            break
        currentPage += 1
    return obtainedProducts


def addShoeProductFeatureValuesSVD(
    initiallyParsed: Dict[str, dict],
    productsByFilterKeyword: List,
    shoeProductFeature: str,
    value: Union[float, str],
) -> None:
    for product in productsByFilterKeyword:
        id = str(product["id"])
        if (
            shoeProductFeature == "gender" and value == "Men"
        ):  # Adjust gender for consistency
            value = "Man"
        elif shoeProductFeature == "gender" and value == "Men & Women":
            value = ["Man", "Woman"]
        try:
            if shoeProductFeature == "shoeSize":
                initiallyParsed[id][shoeProductFeature]["us"].add(value)
            elif shoeProductFeature == "gender":
                if isinstance(value, list):
                    for val in value:
                        initiallyParsed[id][shoeProductFeature].add(val)
                else:
                    initiallyParsed[id][shoeProductFeature].add(value)
        except KeyError:
            print(
                "Product with ID {id} with shoeProductFeature {shoeProductFeature} was not found in initial search!".format(
                    id=id, shoeProductFeature=shoeProductFeature
                )
            )


def addAdditionalFilterOptionsForDataSVD(
    website: Website, initiallyParsed: Dict[str, dict]
) -> None:
    """Modifies (adds) additional filterOption for products in dict{eshopId -> product}"""
    queryUrl, filterOptionsForManualRequest, headers = itemgetter(
        "queryUrl", "filterOptionsForManualRequest", "headers"
    )(website.config)
    filterDataToObtain = {}
    t = Template(queryUrl)
    url = t.safe_substitute(currentPageValue="1")
    data = makeRequest(url, headers=headers)
    try:
        if data == None or len(data["data"]["products"]["aggregations"]) == 0:
            return None
        else:
            aggregations = data["data"]["products"]["aggregations"]
    except KeyError as e:
        print(
            "Structure change for getting aggretation info from {}".format(
                website.domain
            )
        )
        print(str(e))
        return None

    # get options for filterKeyword which is mapped to shoeProductFeature
    for key, value in filterOptionsForManualRequest.items():
        for agg in aggregations:
            if agg["attribute_code"] == value:
                options = [op["value"] for op in agg["options"]]
                if key == "shoeSize":
                    options = [op for op in options if not sizeIsRange(op)]
                filterDataToObtain[key] = {value: options}

    # based on filterKeywords and related options update shoeProductFeatures of initiallyObtainedData
    for shoeProductFeature, filterOptionDict in filterDataToObtain.items():
        for filterKeyword, filterValues in filterOptionDict.items():
            for value in filterValues:
                filterUrlPart = createFilterUrlPartSVD(filterKeyword, value)
                productsByFilterKeyword = getProductsSVD(website, filterUrlPart)
                addShoeProductFeatureValuesSVD(
                    initiallyParsed, productsByFilterKeyword, shoeProductFeature, value
                )


def scrape_svd(website: Website) -> Optional[List[ShoeProduct]]:
    obtainedProducts = getProductsSVD(website)
    initiallyParsed = parseInitiallyObtainedDataSVD(obtainedProducts, website)
    addAdditionalFilterOptionsForDataSVD(website, initiallyParsed)
    productsList = createShoeProductList(initiallyParsed)
    return productsList
