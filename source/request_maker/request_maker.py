import asyncio
from typing import List

import requests

from request_maker.request_maker_abstract import RequestMakerAbstract, NotHTML


class RequestMaker(RequestMakerAbstract):
    def __init__(self, timeout: int, allowed_content_types: List[str]) -> None:
        self.timeout: int = 3
        self.allowed_content_types = allowed_content_types

    async def make_get_request(self, url: str) -> str:
        return await asyncio.to_thread(self.get_request_sync, url)

    def get_request_sync(self, url: str) -> str:

        response = requests.head(url, timeout=self.timeout)
        response.raise_for_status()
        for content_type in self.allowed_content_types:
            if response.headers['Content-type'].startswith(content_type):
                break
        else:
            raise NotHTML(f"content-type: {response.headers['Content-type']} not allowed")

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text
