from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigManager:
    client_id: str
    client_secret: str
    redirect_url: str
