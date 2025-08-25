# pyright: reportUnknownVariableType=false
# pyright: reportUnannotatedClassAttribute=false
# pyright: reportUnknownMemberType=false

from typing import Any


from collections import defaultdict
from dataclasses import dataclass
from ada_url import URL
import httpx
from loguru import logger

from pydantic import BaseModel, computed_field

from dotenv import dotenv_values


@dataclass(frozen=True)
class ConfigManager:
    client_id: str  # = "137d27b6e41d488480079bd838daa65c"
    client_secret: str  # = "9d6b5c59e14348b299f751135a7ed9d7"


@dataclass
class SpotifyEndpoints:
    authenticate: URL = "https://accounts.spotify.com/api/token"
    get_playlists: URL = "https://api.spotify.com/v1/me/playlists"


class SpotifyAuthenticationResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: float

    @computed_field
    @property
    def header(self) -> dict[str, str]:
        return {"Authorization": f"{self.token_type} {self.access_token}"}


class NetworkManager:
    def __init__(self):
        self.common_headers: defaultdict[Any, Any] = defaultdict()
        self.client = httpx.Client(headers=self.common_headers)

    def post(self, endpoint: URL, headers: dict[str, str], body: dict[str, str]):
        logger.info(f"POST: {endpoint}")
        response = self.client.post(
            endpoint, headers=headers, data=body
        ).raise_for_status()
        logger.info(response.json())
        return response

    def get(self, endpoint: URL, headers=dict[str, str]) -> Any:
        logger.info(f"GET: {endpoint}")
        response: Any = self.client.get(endpoint, headers=headers).raise_for_status()
        return response


class Storage:
    def __init__(self) -> None:
        self.container: defaultdict[str, Any] = defaultdict()

    def save(self, key: str, data: Any):
        logger.info(f"Saving for key {key} and data {data}")
        self.container[key] = data

    def get(self, key: str):
        logger.info(f"Retrieving data for key {key}")
        return self.container[key]


class SpotifyFetcher:
    def __init__(
        self,
        config_manager: ConfigManager,
        network_manager: NetworkManager,
        storage: Storage,
    ):
        self.config_manager: ConfigManager = config_manager
        self.network_manager: NetworkManager = network_manager
        self.auth_params: SpotifyAuthenticationResponse | None = None
        self.storage: Storage = storage

    def authenticate(self) -> SpotifyAuthenticationResponse:
        logger.info("Authenticating to Spotify")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self.config_manager.client_id,
            "client_secret": self.config_manager.client_secret,
        }
        response = self.network_manager.post(
            SpotifyEndpoints.authenticate, headers=headers, body=body
        )
        auth_params = SpotifyAuthenticationResponse.model_validate(response.json())
        logger.info("Authenticated to Spotify")
        return auth_params

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


def main():
    env_config: dict[str, str] = dotenv_values(".env")
    config_manager = ConfigManager(
        client_id=env_config["spotify_client_id"],
        client_secret=env_config["spotify_client_secret"],
    )
    # pull spotify playlist
    spotify_fetcher = SpotifyFetcher(
        config_manager=config_manager,
        network_manager=NetworkManager(),
        storage=Storage(),
    )

    spotify_fetcher.fetch()

    # Use pydantic to encode reponses and pass around objects

    # Store pulled song into a small file for now or a db eventually ? SQlite or else or a FUCKING HASHMAP


if __name__ == "__main__":
    main()
