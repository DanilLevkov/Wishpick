import json
from bs4 import BeautifulSoup
import logging

api_url = "http://www.ozon.ru/page/json/v2?url="
ozon_prefix = "https://www.ozon.ru"


def is_ozon_link(url: str):
    prefixes = ["https://www.ozon.ru", "https://ozon.ru"]
    return any(url.startswith(pref) for pref in prefixes)


def parse_json(parsed_info):
    inner_html = dict()
    try:
        for val in parsed_info["seo"]["script"]:
            if "innerHTML" in val.keys():
                inner_html = json.loads(val["innerHTML"])
    except (json.decoder.JSONDecodeError, KeyError, AttributeError):
        logging.info("innerHTML loading error")

    gift = dict()
    if not inner_html:
        states = parsed_info["widgetStates"]
        for widget_name, widget_value in states.items():
            if "webProductHeading" in widget_name:
                value = json.loads(widget_value)
                gift["name"] = value.get("title", None)
        logging.info("use widgetStates")
        return gift

    gift["name"] = inner_html.get("name", None)
    gift["img_url"] = inner_html.get("image", None)
    gift["brand"] = inner_html.get("brand", None)
    offer = inner_html.get("offers", None)
    if offer:
        gift["price"] = offer.get("price", None)

    category = parsed_info.get("layoutTrackingInfo", None)
    if category:
        category = json.loads(category)
        cat_list = category["hierarchy"].split("/")
        cat_result = [cat.lower() for cat in cat_list
                      if cat != gift["brand"]
                      if not any(ch in cat for ch in [' ', ','])]
        gift["category"] = cat_result
    return gift


def parse_ozon(driver, url: str):
    if not url.startswith(ozon_prefix + "/product"):
        logging.info(f"Short link is received {url}")
        driver.get(url)
        url = driver.current_url
    if not url.startswith(ozon_prefix + "/product"):
        logging.info(f"Full link is not supported {url}")
        return
    product_url = url.removeprefix(ozon_prefix)
    product_url = product_url.split('/?', 1)[0]
    api_product_url = api_url + product_url
    driver.get(api_product_url)
    response: str = driver.page_source
    if not response:
        logging.info("driver.page_source empty")
        return
    try:
        parsed_html = BeautifulSoup(response, 'html.parser')
        body = parsed_html.body
        if body.pre:
            body = body.pre
        json_response = json.loads(body.text)
        result = parse_json(json_response)
        return result
    except (json.decoder.JSONDecodeError, AttributeError):
        logging.info("HTML parser except")
        return
