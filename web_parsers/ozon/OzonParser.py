import json
import requests
from web_parsers.driver import driver

api_url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2?url="
ozon_prefix = "https://www.ozon.ru"


def parse_json(parsed_info):
    states = parsed_info["widgetStates"]
    gift = {}
    for widget_name, widget_value in states.items():
        if "webProductHeading" in widget_name:
            value = json.loads(widget_value)
            gift["name"] = value["title"]
        if "webSale" in widget_name:
            value = json.loads(widget_value)
            gift["title"] = value["title"]
            gift["price"] = value["finalPrice"]
    return gift


def parse_ozon_item_url(url: str):
    if not url.startswith(ozon_prefix + "/product"):
        return
    product_url = url.removeprefix(ozon_prefix)
    product_url = product_url.split('/?', 1)[0]
    api_product_url = api_url + product_url
    driver.get(api_product_url)
    response: str = driver.page_source
    if not response:
        return
    try:
        json_response = json.loads(response)
        result = parse_json(json_response)
        return result
    except json.decoder.JSONDecodeError:
        return
