import httpx
from loguru import logger
from yarl import URL
from typing import Any, Literal
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

    def build_request(
        self,
        method: Literal["GET", "POST"],
        endpoint: URL,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method, str(endpoint), headers=headers, params=params
        )

    def get(
        self,
        endpoint: URL,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        logger.info(f"GET: {endpoint}, params: {params}")
        response: httpx.Response = self.client.get(
            str(endpoint), headers=headers, params=params
        ).raise_for_status()
        return response
