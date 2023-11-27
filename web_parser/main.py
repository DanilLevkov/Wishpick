import sys
import time
import selenium.webdriver.remote.webdriver
from flask import Flask
from flask import request
import urllib.parse
from urllib3 import exceptions
from selenium import webdriver
from waitress import serve

from credentials.config_reader import config
from ozon.OzonParser import get_ozon_prefix, parse_ozon

app = Flask(__name__)

browser: selenium.webdriver.remote.webdriver.WebDriver = None


def try_init_browser():
    global browser
    try:
        browser = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", options=webdriver.FirefoxOptions())
    except exceptions.MaxRetryError:
        print("Selenium remote connection failed ...", file=sys.stderr)
        return False

    return True


@app.route('/init')
def init_connection():
    global browser
    if not browser:
        while not try_init_browser():
            time.sleep(1)
        print("Browser is connected ...", file=sys.stderr)
    return "Inited"


def parse(url: str):
    if url.startswith(get_ozon_prefix()):
        return parse_ozon(browser, url)


@app.route('/callback')
def parse_and_return():
    url = request.args.get('url', default=None, type=str)
    if not url:
        return
    url = urllib.parse.unquote(url)
    return parse(url)


if __name__ == "__main__":
    serve(app, host=config.web_parser_host, port=config.web_parser_port)
