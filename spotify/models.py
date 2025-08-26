from dataclasses import dataclass
from pydantic import BaseModel, computed_field
from ada_url import URL
from enum import StrEnum


@dataclass(frozen=True)
class SpotifyEndpoints:
    authenticate: URL = URL("https://accounts.spotify.com/api/token")
    get_playlists: URL = URL("https://api.spotify.com/v1/me/playlists")
    authorize_url: URL = URL("https://accounts.spotify.com/authorize")
    token_url: URL = URL("https://accounts.spotify.com/api/token")


class SpotifyTokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class SpotifyAuthenticationResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: float

    @computed_field
    @property
    def header(self) -> dict[str, str]:
        return {"Authorization": f"{self.token_type} {self.access_token}"}


class SpotifyAuthScopes(StrEnum):
    playlist_read_private = "playlist-read-private"
    playlist_read_collaborative = "playlist-read-collaborative"
    user_library_read = "user-library-read"
