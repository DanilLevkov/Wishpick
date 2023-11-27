import time
import selenium.webdriver.remote.webdriver
from flask import Flask
from flask import request
import urllib.parse
from urllib3 import exceptions
from selenium import webdriver
from waitress import serve
import logging

from credentials.config_reader import config
from ozon.OzonParser import is_ozon_link, parse_ozon

app = Flask(__name__)

browser: selenium.webdriver.remote.webdriver.WebDriver = None


def try_init_browser():
    global browser
    try:
        browser = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", options=webdriver.FirefoxOptions())
    except exceptions.MaxRetryError:
        logging.warning("Selenium remote connection failed ...")
        return False

    return True


@app.route('/init')
def init_connection():
    global browser
    if not browser:
        while not try_init_browser():
            time.sleep(1)
        logging.info("Browser is connected ...")
    return "Inited"


def parse(url: str):
    if is_ozon_link(url):
        return parse_ozon(browser, url)
    logging.warning(f"Unsupported url source {url}")


@app.route('/callback')
def parse_and_return():
    url = request.args.get('url', default=None, type=str)
    if not url:
        logging.warning(f"Failed to get url from {request.args}")
        return
    url = urllib.parse.unquote(url)
    logging.info(f"Parsing {url} ...")
    result = parse(url)
    if not result:
        return "Failed", 501
    return result


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    serve(app, host=config.web_parser_host, port=config.web_parser_port)
