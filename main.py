# pyright: reportUnknownVariableType=false
# pyright: reportUnannotatedClassAttribute=false
# pyright: reportUnknownMemberType=false

from math import log
from loguru import logger

from dotenv import dotenv_values

from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from common.storage import Storage
from spotify.fetcher import Fetcher
from spotify.authenticator import Authenticator


def main():
    logger.info("Starting")
    env_config: dict[str, str] = dotenv_values(".env")
    config_manager = ConfigManager(
        client_id=env_config["spotify_client_id"],
        client_secret=env_config["spotify_client_secret"],
        redirect_url=env_config["spotify_redirect_url"],
    )
    # pull spotify playlist
    network_manager: NetworkManager = NetworkManager()
    storage: Storage = Storage()
    spotify_fetcher = Fetcher(
        config_manager=config_manager,
        authenticator=Authenticator(
            config_manager=config_manager, network_manager=network_manager
        ),
        network_manager=network_manager,
        storage=storage,
    )

    spotify_fetcher.fetch()

    # Store pulled song into a small file for now or a db eventually ? SQlite or else or a FUCKING HASHMAP


if __name__ == "__main__":
    main()
