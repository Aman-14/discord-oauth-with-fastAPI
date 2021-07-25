from decouple import config

from .database import db
from .redis import Redis


class Discord:
    NAME = "discord"
    BASE_URL = config("DISCORD_API_BASE_URL")
    OAUTH_APP_CONFIG = {
        "authorize_url": f"{BASE_URL}/oauth2/authorize",
        "access_token_url": f"{BASE_URL}/oauth2/token",
        "scope": "guilds identify email",
    }
