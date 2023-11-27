import aiohttp
import asyncio
import urllib.parse

from credentials.config_reader import config


class URLParser:
    def __init__(self, host: str, port: str):
        self._session = None
        self._api_url = "http://" + host + ":" + port
        self._init_url = self._api_url + "/init"
        self._callback_url = self._api_url + "/callback?"

    def start_session(self):
        self._session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    async def init_connection(self):
        async with self._session.get(self._init_url) as resp:
            return await resp.text()

    async def wait_response(self, url: str):
        request = self._callback_url + urllib.parse.urlencode({"url": url})
        async with self._session.get(request) as resp:
            if resp.status != 200:
                return
            return await resp.json()


url_parser = URLParser(str(config.web_parser_host), str(config.web_parser_port))
