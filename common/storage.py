from loguru import logger
from collections import defaultdict
from typing import Any


class Storage:
    def __init__(self) -> None:
        self.container: defaultdict[str, Any] = defaultdict()

    def save(self, key: str, data: Any):
        logger.info(f"Saving for key {key} and data {data}")
        self.container[key] = data

    def get(self, key: str):
        logger.info(f"Retrieving data for key {key}")
        return self.container[key]
