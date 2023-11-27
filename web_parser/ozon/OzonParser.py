import json
from bs4 import BeautifulSoup

api_url = "http://www.ozon.ru/page/json/v2?url="
ozon_prefix = "https://www.ozon.ru"

def get_ozon_prefix():
    return ozon_prefix

def parse_json(parsed_info):
    inner_html = dict()
    try:
        for val in parsed_info["seo"]["script"]:
            if "innerHTML" in val.keys():
                inner_html = json.loads(val["innerHTML"])
    except (json.decoder.JSONDecodeError, KeyError, AttributeError):
        print("innerHTML loading error")

    gift = dict()
    if not inner_html:
        states = parsed_info["widgetStates"]
        for widget_name, widget_value in states.items():
            if "webProductHeading" in widget_name:
                value = json.loads(widget_value)
                gift["name"] = value.get("title", None)
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
        driver.get(url)
        url = driver.current_url
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
