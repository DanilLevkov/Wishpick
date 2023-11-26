import json
from web_parsers.driver import driver
from bs4 import BeautifulSoup

api_url = "http://www.ozon.ru/page/json/v2?url="
ozon_prefix = "https://www.ozon.ru"


def parse_json(parsed_info):
    states = parsed_info["widgetStates"]
    gift = {}
    for widget_name, widget_value in states.items():
        if "webProductHeading" in widget_name:
            value = json.loads(widget_value)
            gift["name"] = value.get("title", None)
        if "webSale" in widget_name:
            value = json.loads(widget_value)
            price = value.get("price", None)
            if price:
                price = int(price) / 100
                gift["price"] = price
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
        parsed_html = BeautifulSoup(response, 'html.parser')
        pre = parsed_html.body.pre
        if not pre:
            return
        json_response = json.loads(pre.text)
        result = parse_json(json_response)
        return result
    except (json.decoder.JSONDecodeError, AttributeError):
        return
