from website import Website
from schemas import FilterOptions, ShoeProduct, createShoeProduct
from typing import Dict, List, Union
from utils import floatOrIntFromStr, makeRequest, tryToFloatConversion
import urllib.parse
from string import Template
from schemas import createShoeProduct

# SIVASDESCALZO
MAX_REQUESTS = 30


def createFilterUrlPartSVD(filterKeyword: str, value: str) -> str:
    toEncode = f'"{filterKeyword}":{{"eq":"{value}"}}'
    toEncode = toEncode + ","
    return urllib.parse.quote(toEncode)


def parseInitiallyObtainedDataSVD(
    data: List[dict], website: Website
) -> Dict[str, FilterOptions]:
    output = {}
    for product in data:
        eshopID = str(product["id"])
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
        productData["shoeSize"] = []
        productData["gender"] = []
        productData["eshopID"] = eshopID
        productData["domain"] = website.domain
        shoeProduct = createShoeProduct(productData)
        if shoeProduct != None:
            output[eshopID] = productData
    return output


def getProductsSVD(website: Website, filterUrlPart: str = None) -> List:
    obtainedProducts = []
    url = website.queryUrl if filterUrlPart == None else website.queryUrlWithFilters
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
        data = makeRequest(url, website.domain)
        if data == None or len(data["data"]["products"]["items"]) == 0:
            break
        else:
            obtainedProducts += data["data"]["products"]["items"]
        currentPage += 1
    return obtainedProducts


def addShoeProductFeatureValuesSVD(
    initiallyParsed: Dict[str, FilterOptions],
    productsByFilterKeyword: List,
    shoeProductFeature: str,
    value: Union[float, str],
) -> None:
    for product in productsByFilterKeyword:
        id = str(product["id"])
        try:
            initiallyParsed[id][shoeProductFeature].append(value)
        except KeyError:
            print(
                "Product with ID {id} with shoeProductFeature {shoeProductFeature} was not found in initial search!".format(
                    id=id, shoeProductFeature=shoeProductFeature
                )
            )


def addAdditionalFilterOptionsForDataSVD(
    website: Website, initiallyParsed: Dict[str, FilterOptions]
) -> List[ShoeProduct]:
    filterDataToObtain = {}
    t = Template(website.queryUrl)
    url = t.safe_substitute(currentPageValue="1")
    data = makeRequest(url, website.domain)
    if data == None or len(data["data"]["products"]["aggregations"]) == 0:
        return None
    else:
        aggregations = data["data"]["products"]["aggregations"]
    # get options for filterKeyword which is mapped to shoeProductFeature
    for key, value in website.filterOptionsForManualRequest.items():
        for agg in aggregations:
            if agg["attribute_code"] == value:
                options = [op["value"] for op in agg["options"]]
                if key == "shoeSize":
                    options = [
                        floatOrIntFromStr(op)
                        for op in options
                        if tryToFloatConversion(op) != None
                    ]  # Hardcoded for shoeProductFeature :/
                print(options)
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
    return list(initiallyParsed.values())


def getAllDataSVD(website: Website) -> List:
    obtainedProducts = getProductsSVD(website)
    initiallyParsed = parseInitiallyObtainedDataSVD(obtainedProducts, website)
    output = addAdditionalFilterOptionsForDataSVD(website, initiallyParsed)
    return output


###################
