from loguru import logger
from collections import defaultdict
from typing import Any
import json
from pathlib import Path


class Storage:
    def __init__(self, root_dir: Path) -> None:
        self.filename: str = "storage.json"
        self.root_dir: Path = root_dir
        self.file_path: Path = self.root_dir / self.filename
        self.container: defaultdict[str, Any] = defaultdict(dict)

        self._initialize_container()

    def _initialize_container(self) -> None:
        """Initialize the container with data from disk if available."""
        try:
            data = self.read_from_disk()
            if data:
                self.container.update(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to read from disk: {e}")

    def save(self, key: str, data: Any, overwrite: bool = False):
        logger.info(f"Saving for key {key} and data {data}, overwrite {overwrite}")
        key_exist: bool = key in self.container
        if overwrite or not key_exist:
            self.container[key] = data
            self.write_to_disk()

    def get(self, key: str) -> Any:
        logger.info(f"Retrieving data for key {key}")
        return self.container.get(key)

    def write_to_disk(self) -> None:
        logger.info("Writing to disk")
        with open(self.file_path, "w") as f:
            _ = f.write(json.dumps(self.container))

    def read_from_disk(self) -> dict[str, Any]:
        logger.info("Reading from disk")
        with open(file=self.file_path, mode="r") as f:
            return json.loads(f.read())
