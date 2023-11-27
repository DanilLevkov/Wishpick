from flask import Flask

import time
from credentials.config_reader import config

app = Flask(__name__)


@app.route('/')
def ping_service():
    return 'Hello, I am ping service!'

def parse(url: str):
    if url.startswith(get_ozon_prefix()):
        return parse_ozon(driver, url)


@app.route('/callback')
def parse_and_return():
    url = request.args.get('url', default=None, type=str)
    if not url:
        return
    url = urllib.parse.unquote(url)
    return parse(url)


if __name__ == "__main__":
    app.run(host=config.web_parser_host, port=config.web_parser_port, debug=True)
