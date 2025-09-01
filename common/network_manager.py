import httpx
from loguru import logger
from ada_url import URL
from typing import Any
from collections import defaultdict


class NetworkManager:
    def __init__(self):
        self.common_headers: defaultdict[Any, Any] = defaultdict()
        self.client: httpx.Client = httpx.Client(headers=self.common_headers)

    def post(
        self,
        endpoint: URL,
        headers: dict[str, str] | None = None,
        body: dict[str, str] | None = None,
    ) -> httpx.Response:
        logger.info(f"POST: {endpoint}")
        response: httpx.Response = self.client.post(
            str(endpoint), headers=headers, data=body
        ).raise_for_status()
        logger.info(response.json())
        return response

    def get(
        self,
        endpoint: URL,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        logger.info(f"GET: {endpoint}")
        response: httpx.Response = self.client.get(
            str(endpoint), headers=headers, params=params
        ).raise_for_status()
        logger.info(f"{response.json()}")
        return response
