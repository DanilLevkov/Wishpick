from flask import Flask

import time
from credentials.config_reader import config

app = Flask(__name__)


@app.route('/')
def ping_service():
    return 'Hello, I am ping service!'


@app.route('/ping')
def do_ping():
    time.sleep(3)
    return "Ping pong"


if __name__ == "__main__":
    app.run(host=config.web_parser_host, port=config.web_parser_port, debug=True)
