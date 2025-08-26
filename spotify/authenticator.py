import secrets
import base64
import httpx
from loguru import logger

from spotify.models import (
    SpotifyEndpoints,
    SpotifyTokenResponse,
    SpotifyAuthScopes,
    SpotifyAuthenticationResponse,
)

from common.config_manager import ConfigManager
from common.network_manager import NetworkManager


class Authenticator:
    def __init__(self, config_manager: ConfigManager, network_manager: NetworkManager):
        self.config_manager: ConfigManager = config_manager
        self.network_manager: NetworkManager = network_manager
        self.state: str = secrets.token_hex()

    def request_user_authorization(self):
        scope: str = SpotifyAuthScopes.playlist_read_private
        params: dict[str, str] = {
            "response_type": "code",
            "client_id": self.config_manager.client_id,
            "scope": scope,
            "redirect_uri": self.config_manager.redirect_url,
            "state": self.state,
        }
        _ = self.network_manager.get(SpotifyEndpoints.authorize_url, params=params)

    def request_access_token(self, code: str, state: str) -> SpotifyTokenResponse:
        if state != self.state:
            raise ValueError("State values are different - tampering alert")
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config_manager.redirect_url,
        }
        # All of those shenanigans are to encode a byte-str not a string to base64
        authorization_header: str = base64.b64encode(
            f"{self.config_manager.client_id}:{self.config_manager.client_secret}".encode()
        ).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {authorization_header}",
        }
        # Can I do some type forwarding ? so that I do not leak httpx.response ?
        response: httpx.Response = self.network_manager.post(
            SpotifyEndpoints.token_url, headers=headers, body=params
        )
        auth_result: SpotifyTokenResponse = SpotifyTokenResponse.model_validate(
            response.json()
        )
        return auth_result

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
