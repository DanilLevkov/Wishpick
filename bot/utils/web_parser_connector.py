import aiohttp
import asyncio
import urllib.parse

from credentials.config_reader import config


class URLParser:
    def __init__(self, host: str, port: str, inside_docker: bool):
        self._session = None
        self._api_url = "http://" + host + ":" + port
        self._init_url = self._api_url + "/init"
        self._callback_url = self._api_url + "/callback?"
        self._is_stub = not inside_docker

    def start_session(self):
        if self._is_stub:
            return
        self._session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    async def init_connection(self):
        if self._is_stub:
            return "Stub"
        async with self._session.get(self._init_url) as resp:
            return await resp.text()

    async def wait_response(self, url: str):
        if self._is_stub:
            return "stub"
        request = self._callback_url + urllib.parse.urlencode({"url": url})
        async with self._session.get(request) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 501:
                return "empty"
            return "failed"


url_parser = URLParser(str(config.web_parser_host), str(config.web_parser_port), config.inside_docker)
