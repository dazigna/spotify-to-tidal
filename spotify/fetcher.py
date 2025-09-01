from loguru import logger
from typing import Any
import json
from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from common.storage import Storage

from spotify.models import SpotifyTokenResponse, SpotifyEndpoints


class Fetcher:
    def __init__(
        self,
        config_manager: ConfigManager,
        network_manager: NetworkManager,
        storage: Storage,
    ):
        self.config_manager: ConfigManager = config_manager
        self.network_manager: NetworkManager = network_manager
        self.storage: Storage = storage

        auth_content = json.loads(self.storage.get("spotify_auth"))
        logger.info(f"Auth content: {auth_content}")
        if not auth_content:
            raise ValueError("The user is not authenticated - run the auth flow")
        self.auth_params: SpotifyTokenResponse = SpotifyTokenResponse.model_validate(
            auth_content
        )

    def fetch_playlists(self) -> Any:
        response = self.network_manager.get(
            endpoint=SpotifyEndpoints.get_playlists, headers=self.auth_params.header
        )

        logger.info(f"Fetch playlist: {response.json()}")
        return response

    def fetch(self):
        playlists = self.fetch_playlists()
        # self.storage.save("playlist", playlists)
