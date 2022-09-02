from scraping.website import Website
from scraping.schemas import ShoeProduct, createShoeProduct, createShoeSize
from typing import List
from scraping.utils import makeRequest, sizeIsRange
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


def getAllProductsInfoFS(website: Website) -> dict:
    productsInfo, headers = itemgetter("productsInfo", "headers")(website.config)
    for gender in productsInfo:
        res = makeRequest(
            productsInfo[gender]["infoUrl"],
            website.domain,
            headers=headers,
        )
        if res == None:
            print(
                "Unable to get product data for {}".format(
                    productsInfo[gender]["infoUrl"]
                )
            )
            continue
        try:
            info = productsInfo[gender]["info"]
            info["total"] = res["products"]["total"]
            info["page"] = res["products"]["pagination"]["page"]
            info["total_pages"] = res["products"]["pagination"]["total_pages"]
            info["items_per_page"] = res["products"]["pagination"]["items_per_page"]
            sizesDict = {}
            for x in res["filters"]["size"]["collections"]:
                sizes = [
                    size["name"] for size in x["items"] if not sizeIsRange(size["name"])
                ]
                if x["name"] == "US":
                    sizesDict["us"] = {"filterKeyword": "us", "sizes": sizes}
                elif x["name"] == "EUR":
                    sizesDict["eu"] = {"filterKeyword": "eur", "sizes": sizes}
            info["sizes"] = sizesDict

        except KeyError as e:
            print("Change in structure of getting info about FS product information!")
            print(str(e))
            del productsInfo[gender]
        except StopIteration as e:
            print("Change in structure of getting US sizes from FS!")
            print(str(e))
            del productsInfo[gender]
    return productsInfo


def extractDataFromFSResponse(
    productsDict: dict, website: Website, response: dict, gender: str
) -> None:
    """Extracts data from response and modifies productsDict dictionary.
    If product is already in dict (product was found by ID from eshop)
    than only gender for product is appended, otherwise new product is
    added to the dict.
    """
    try:
        items = response["products"]["items"]
        for product in items:
            productData = {}
            eshopId = product["id"]
            productFromDict = productsDict.get(eshopId)
            if productFromDict == None:  # product was not scraped so far
                productData["brandName"] = product["manufacturer"]["name"]
                productData["name"] = product["title"]
                productData["shoeId"] = product["code"]
                productData["smallImageUrl"] = product["image"]
                productData["url"] = website.domain + product["url"]
                productData["finalPrice"] = product["price"]["value"]
                productData["originalPrice"] = None
                productData["percentOff"] = product["sale"]["percents"]
                productData["shoeSize"] = {"us": set(), "eu": set()}
                productData["outOfStock"] = product["sold_out"]
                productData["gender"] = [gender]
                productData["eshopId"] = eshopId
                productData["domain"] = website.domain
                productsDict[eshopId] = productData
            else:  # product was already scraped so append only gender - do not care about url
                productFromDict["gender"].append(gender)
    except KeyError as e:
        print("Structure for extracting data from FS response has changed!")
        print(str(e))


def getListOfProductIdsFromFSResponse(website: Website, response: dict) -> list:
    try:
        return [item["id"] for item in response["products"]["items"]]
    except KeyError as e:
        print(
            "Structure for extracting product ID from {} response has changed!".format(
                website.customName
            )
        )
        print(str(e))
        return []


def convertSizeForUrl(size: str):
    size = size.replace(" ", "%20")
    size = size.replace("/", "|")
    return size


def assignSizesToProducts(
    website: Website, productsDict: dict, productsInfo: dict
) -> None:
    """
    Modifies productsDict -> assigns scraped sizes to existing products
    """
    headers = itemgetter("headers")(website.config)
    for gender in productsInfo:
        sizesDict = productsInfo[gender]["info"]["sizes"]
        productsBySizeUrl = productsInfo[gender]["productsBySizeUrl"]
        headers["Referer"] = productsInfo[gender]["infoUrl"]
        for shoeSizeAttr, sizeMetric in sizesDict.items():
            sizes = sizeMetric["sizes"]
            filterKeyword = sizeMetric["filterKeyword"]
            for size in sizes:
                currentPage = 1
                while currentPage < MAX_REQUESTS:
                    print(
                        productsBySizeUrl.format(
                            filterKeyword, convertSizeForUrl(size), currentPage
                        )
                    )
                    res = makeRequest(
                        productsBySizeUrl.format(
                            filterKeyword, convertSizeForUrl(size), currentPage
                        ),
                        website.domain,
                        headers=headers,
                    )
                    if res == None:
                        break
                    ids = getListOfProductIdsFromFSResponse(website, res)
                    for id in ids:
                        if productsDict.get(id) != None:
                            productsDict[id]["shoeSize"][shoeSizeAttr].add(size)
                        else:
                            print(
                                "Product with eshopId {} was not found in initial search! - {}".format(
                                    id, website.domain
                                )
                            )
                    try:
                        if currentPage >= res["products"]["pagination"]["total_pages"]:
                            break
                    except KeyError as e:
                        print(
                            "Structure for extracting total_pages when filtering by size from {} response has changed!".format(
                                website.customName
                            )
                        )
                        print(str(e))
                        break
                    currentPage += 1


def getProductsFS(productsInfo: dict, website: Website) -> dict:
    headers = itemgetter("headers")(website.config)
    productsDict = {}
    for gender in productsInfo:
        info = productsInfo[gender]["info"]
        productsUrl = productsInfo[gender]["productsUrl"]
        headers["Referer"] = productsInfo[gender]["infoUrl"]
        currentPage = info["page"]
        totalPages = info["total_pages"]
        for i in range(currentPage, totalPages + 1):
            print(productsUrl.format(i))
            res = makeRequest(productsUrl.format(i), website.domain, headers=headers)
            extractDataFromFSResponse(productsDict, website, res, gender)
    return productsDict


def scrape_fs(website: Website) -> List[ShoeProduct]:
    productsInfo = getAllProductsInfoFS(website)
    productsDict = getProductsFS(productsInfo, website)
    assignSizesToProducts(website, productsDict, productsInfo)
    shoeProductList = createShoeProductList(productsDict)
    return shoeProductList
