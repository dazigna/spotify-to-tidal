from loguru import logger
from typing import Any

from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from common.storage import Storage

from spotify.authenticator import Authenticator
from spotify.models import SpotifyAuthenticationResponse, SpotifyEndpoints


class Fetcher:
    def __init__(
        self,
        config_manager: ConfigManager,
        authenticator: Authenticator,
        network_manager: NetworkManager,
        storage: Storage,
    ):
        self.config_manager: ConfigManager = config_manager
        self.authenticator: Authenticator = authenticator
        self.network_manager: NetworkManager = network_manager
        self.auth_params: SpotifyAuthenticationResponse | None = None
        self.storage: Storage = storage

    def fetch_playlists(self) -> Any:
        response = self.network_manager.get(
            endpoint=SpotifyEndpoints.get_playlists, headers=self.auth_params.header
        )

        logger.info(f"Fetch playlist: {response}")
        return response

    def fetch(self):
        self.auth_params = self.authenticate()
        playlists = self.fetch_playlists()
        self.storage.save("playlist", playlists)
