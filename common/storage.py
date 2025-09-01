from loguru import logger
from collections import defaultdict
from typing import Any


class Storage:
    def __init__(self) -> None:
        self.container: defaultdict[str, Any] = defaultdict()

    def save(self, key: str, data: Any, overwrite: bool = False):
        logger.info(f"Saving for key {key} and data {data}, overwrite {overwrite}")
        key_exist: bool = self.container.get(key) is not None
        if overwrite or not key_exist:
            self.container[key] = data

    def get(self, key: str) -> Any:
        logger.info(f"Retrieving data for key {key}")
        return self.container.get(key)
