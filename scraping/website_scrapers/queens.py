from json import JSONDecodeError
from typing import Dict, List, Literal, Optional, Set
from bs4 import BeautifulSoup, Tag
from scraping.schemas import ShoeProduct, createShoeProduct, createShoeSize
from scraping.utils import make_request
from scraping.website import Website
from . import MAX_REQUESTS


class ShoeSizeExtractionError(Exception):
    pass


class ParsingProductPageHtmlError(Exception):
    pass


# UTILS
def get_float_price(price: str) -> float:
    price_string = price.split()[0]
    return float(price_string.replace(",", "."))


def create_shoe_sizes_dict(sizes: str) -> Dict[str, set]:
    # patter for sizes is 'US 7.5 (eur 40 2/3)'
    shoe_sizes = {"us": set(), "eu": set(), "cm": set(), "uk": set()}
    for size in sizes:
        split_sizes = size.split("(")
        for size_to_parse in split_sizes:
            size_to_parse = size_to_parse.replace("(", "").replace(")", "")
        try:
            if "us" in size_to_parse.casefold():
                shoe_sizes["us"].add(size_to_parse.split(" ", 1)[1].strip())
            if "eur" in size_to_parse.casefold():
                shoe_sizes["eu"].add(size_to_parse.split(" ", 1)[1].strip())
        except IndexError:
            raise ShoeSizeExtractionError()
    return shoe_sizes


def union_two_sizes_dicts(
    dict_1: Dict[str, Set], dict_2: Dict[str, Set]
) -> Dict[str, Set]:
    new_sizes_dict = {"us": set(), "eu": set(), "cm": set(), "uk": set()}
    new_sizes_dict["us"].union(dict_1["us"], dict_2["us"])
    new_sizes_dict["eu"].union(dict_1["eu"], dict_2["eu"])
    return new_sizes_dict


def create_shoe_products(product_dicts: List[dict]) -> List[ShoeProduct]:
    shoeProductList = []
    for product in product_dicts:
        shoeSize = createShoeSize(product["shoeSize"])
        if shoeSize == None:
            continue
        product["shoeSize"] = shoeSize
        shoeProductList.append(createShoeProduct(product))
    return list(filter(None, shoeProductList))


def update_already_scraped_product(
    product: dict,
    product_page_html: str,
    gender: Literal["Man", "Woman", "Kids"],
    product_url: str,
) -> None:
    product_sizes = get_product_size_dict_from_product_page(
        product_page_html, product_url
    )
    if product_sizes == None:
        return
    product["gender"].add(gender)
    product["shoeSize"] = union_two_sizes_dicts(
        product["shoeSize"],
        product_sizes,
    )
    product["outOfStock"] = (
        True
        if (
            len(product["shoeSize"]["us"])
            + len(product["shoeSize"]["eu"])
            + len(product["shoeSize"]["cm"])
            + len(product["shoeSize"]["uk"])
        )
        == 0
        else False
    )


class ProductHref:
    def __init__(
        self,
        gender: Literal["Man", "Woman", "Kids"],
        product_href: str,
        eshop_product_id: str,
    ):
        self.gender = gender
        self.product_href = product_href
        self.eshop_product_id = eshop_product_id


######


def get_product_size_dict_from_product_page(
    product_page_html: str, product_page_url: str
) -> Optional[dict]:
    soup = BeautifulSoup(product_page_html, "html.parser")
    item_info_div = soup.find("div", class_="item-info")
    if item_info_div == None:
        return None
    select = item_info_div.find("select", class_="form-control", id="variant")
    if select == None:
        return create_shoe_sizes_dict([])
    options = select.find_all("option", recursive=False)
    size_options_string_list = [op.text for op in options]
    try:
        shoe_sizes_dict = create_shoe_sizes_dict(size_options_string_list)
    except ShoeSizeExtractionError:
        print("Unable to extract sizes for {}".format(product_page_url))
        return None
    return shoe_sizes_dict


def aggregate_product_hrefs(
    url_for_hrefs: str, gender: Literal["Man", "Woman", "Kids"]
) -> List[ProductHref]:
    hrefs = []
    current_page = 1
    is_last_page = False
    while is_last_page is False and current_page <= MAX_REQUESTS:
        url = url_for_hrefs.format(current_page)
        print("Making request to {}".format(url))
        res = make_request(url)
        if res.status_code < 200 or res.status_code > 299:
            print(
                "Status code {} for request {} - unable to gather hrefs".format(
                    res.status_code, url
                )
            )
            continue
        elif res == None:
            continue
        try:
            res_json = res.json()
            res_html = res_json["html"]
            is_last_page = res_json["is_last_page"]
            soup = BeautifulSoup(res_html, "html.parser")
            a_tags = soup.find_all("a", {"data-id": lambda val: val is not None})
            for link in a_tags:
                hrefs.append(ProductHref(gender, link["href"], link["data-id"]))
            current_page += 1
        except JSONDecodeError:
            print("Unable to load response as json from url {}".format(url))
            return hrefs
        except KeyError as e:
            print(
                "Structure for acquiring hrefs from {} has changed, Error: {}".format(
                    url_for_hrefs, e
                )
            )
            return hrefs
    return hrefs


def get_product_hrefs_by_gender(website: Website) -> List[ProductHref]:
    config = website.config
    genders = ["Man", "Woman", "Kids"]
    product_hrefs = []
    for gender in genders:
        url_for_hrefs = config[gender]["url"]
        product_hrefs += aggregate_product_hrefs(url_for_hrefs, gender)
    return product_hrefs


def create_shoe_product_dict_from_product_page_html(
    product_page_html: str,
    gender: Literal["Man", "Woman", "Kids"],
    domain: str,
    product_url: str,
) -> Optional[dict]:
    """
    Creates dict for ShoeProduct schema based on html layout on the page.
    """
    soup = BeautifulSoup(product_page_html, "html.parser")
    item_info_div = soup.find("div", class_="item-info")
    if item_info_div == None:
        print("Cannot obtain item info for {}".format(product_url))
        return None
    try:
        h1 = item_info_div.find("h1")
        # get a tag with brand name in it and remove it
        a_with_brand_name = h1.find(
            "a", {"title": lambda title: title is not None}
        ).extract()
        brand_name = a_with_brand_name.text
        # remove small tag with cws from h1 if exists
        if h1.small:
            h1.small.extract()
        # merge all left content from h1 into product name (+ strip of white spaces)
        product_name_list = []
        for content in h1.contents:
            if isinstance(content, Tag) and content.name == "a":
                product_name_list.append(content.text.strip())
            elif isinstance(content, str):
                product_name_list.append(content.strip())
        product_name = " ".join(product_name_list).strip()
        # get unique shoe id
        shoe_id = item_info_div.find("p", class_=None).text
        # get eshop shoe id
        eshop_shoe_id_text = item_info_div.find("p", class_="code").span.text
        eshop_shoe_id = (
            eshop_shoe_id_text.split()[-1]
            if "Kód výrobku:" in eshop_shoe_id_text
            else None
        )
        # get image url
        item_carousel = soup.find("div", id="itemCarousel", class_="slider-detail")
        image_url = item_carousel.find("a", class_="rsImg")["href"]
        # get final price (possibly original with percent off), get only number (without currency symbol), replace comma (if any) and try to convert to float
        percent_off = None
        original_price = None
        spans = item_info_div.findAll(
            "span",
            {"class": None, "style": lambda style: style is not None},
            recursive=False,
        )
        span_with_price = next(
            filter(lambda span: len(span.findAll()) == 0, spans), None
        )
        if span_with_price is None:
            span_with_price = item_info_div.find(
                "span", class_="price", recursive=False
            )
            original_price = get_float_price(span_with_price.find("del").text)
        final_price = get_float_price(span_with_price.contents[-1])
        if original_price:
            percent_off = round((1 - final_price / original_price), 2)
        # get shoe sizes us and eu
        shoe_sizes_dict = get_product_size_dict_from_product_page(
            product_page_html, product_url
        )
        if shoe_sizes_dict == None:
            print("Unable to extract sizes for {}".format(product_url))
            return None
        # out of stock is always False
        out_of_stock = (
            True
            if (
                len(shoe_sizes_dict["us"])
                + len(shoe_sizes_dict["eu"])
                + len(shoe_sizes_dict["cm"])
                + len(shoe_sizes_dict["uk"])
            )
            == 0
            else False
        )
    except (AttributeError, IndexError) as e:
        raise ParsingProductPageHtmlError(
            "Error when parsing html product page {} - error: {}".format(product_url, e)
        )

    product_dict = {
        "brandName": brand_name,
        "name": product_name,
        "shoeId": shoe_id,
        "smallImageUrl": image_url,
        "url": product_url,
        "finalPrice": final_price,
        "originalPrice": original_price,
        "percentOff": percent_off,
        "outOfStock": out_of_stock,
        "shoeSize": shoe_sizes_dict,
        "gender": set({gender}),
        "eshopId": eshop_shoe_id,
        "domain": domain,
    }
    return product_dict


def get_product_dicts_from_product_hrefs(product_hrefs: List[ProductHref], domain: str):
    products_by_eshop_id: List[dict] = {}
    for product_href in product_hrefs:
        gender = product_href.gender
        href = product_href.product_href
        eshop_product_id = product_href.eshop_product_id
        product_url = domain + href
        print("Making request to {}".format(product_url))
        res = make_request(product_url)
        if res.status_code < 200 or res.status_code > 299:
            print(
                "Status code {} for request {} - unable to gather product page".format(
                    res.status_code, product_url
                )
            )
            continue
        elif res == None:
            continue
        if res.headers["content-type"] != "text/html; charset=UTF-8":
            print(
                "Content type for product page {} has been changed to {}".format(
                    product_url, res.headers["content-type"]
                )
            )
            continue
        # check if product was already scraped
        if products_by_eshop_id.get(eshop_product_id) != None:
            product = products_by_eshop_id.get(eshop_product_id)
            update_already_scraped_product(product, res.content, gender, product_url)
        # product is not scraped yet
        else:
            try:
                product_dict = create_shoe_product_dict_from_product_page_html(
                    res.content, gender, domain, product_url
                )
                if product_dict == None:
                    continue
                products_by_eshop_id[eshop_product_id] = product_dict
            except ParsingProductPageHtmlError as e:
                print(e)
        break
    return products_by_eshop_id.values()


def scrape_queens(website: Website) -> List[ShoeProduct]:
    product_hrefs = get_product_hrefs_by_gender(website)
    product_dicts = get_product_dicts_from_product_hrefs(product_hrefs, website.domain)
    return create_shoe_products(product_dicts)
