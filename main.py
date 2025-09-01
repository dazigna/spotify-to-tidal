# pyright: reportUnknownVariableType=false
# pyright: reportUnannotatedClassAttribute=false
# pyright: reportUnknownMemberType=false

from threading import Thread

from time import sleep
from typing import override

from loguru import logger

from dotenv import dotenv_values

from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from common.storage import Storage
from spotify.fetcher import Fetcher
from spotify.authenticator import Authenticator
from common.auth_server import SimpleAuthServer


def config_manager_factory() -> ConfigManager:
    env_config: dict[str, str] = dotenv_values(".env")
    config_manager = ConfigManager(
        client_id=env_config["spotify_client_id"],
        client_secret=env_config["spotify_client_secret"],
        redirect_url=env_config["spotify_redirect_url"],
        cert_file=env_config["cert_file_path"],
        key_file=env_config["key_file_path"],
    )
    return config_manager


class ServerThread(Thread):
    def __init__(self, storage: Storage):
        super().__init__()
        logger.info("Creation server thread")
        config_manager: ConfigManager = config_manager_factory()
        network_manager: NetworkManager = NetworkManager()
        self.auth_server: SimpleAuthServer = SimpleAuthServer(
            config_manager=config_manager,
            network_manager=network_manager,
            storage=storage,
        )

    @override
    def run(self):
        logger.info("Start serving")
        self.auth_server.serve()

    def shutdown(self):
        logger.info("shutting down server thread")
        self.auth_server.shutdown()
        self.join()
        logger.info("Server has been shut down.")


def start_server_in_background(storage: Storage):
    server_thread = ServerThread(storage=storage)
    server_thread.start()
    return server_thread


def main():
    storage: Storage = Storage()
    logger.info("Starting")
    server_thread: Thread = start_server_in_background(storage=storage)

    logger.info("Server has started - ready")

    try:
        config_manager: ConfigManager = config_manager_factory()

        network_manager: NetworkManager = NetworkManager()

        authenticator = Authenticator(
            config_manager=config_manager,
            network_manager=network_manager,
            storage=storage,
        )

        authenticator.request_user_authorization()

    except KeyboardInterrupt:
        logger.info("shutting down")
        server_thread.shutdown()
        logger.info("shut down complete")


if __name__ == "__main__":
    main()
