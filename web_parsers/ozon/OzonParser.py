import json
import requests

from objects.gift import GiftItem

api_url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2?url="
ozon_prefix = "https://www.ozon.ru"

def get_response(url, json_url):
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.headers = header
    response = session.get(url)
    if response.status_code != 200:
        return None
    json_response = session.get(json_url)
    if json_response.status_code != 200:
        return None
    return json_response.json()


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
        return "not a product"
    product_url = url.removeprefix(ozon_prefix)
    product_url = product_url.split('/?', 1)[0]
    api_product_url = api_url + product_url
    response = get_response(url, api_product_url)
    json_response = response.json()
    result = parse_json(json_response)
    return result
