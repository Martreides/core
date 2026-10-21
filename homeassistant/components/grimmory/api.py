"""Minimal Grimmory API client."""

import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

_LOGGER = logging.getLogger(__name__)


class GrimmoryApiClient:
    """Minimal Grimmory API client."""

    def __init__(self, host: str | None = None, token: str | None = None) -> None:
        """Initialize the Grimmory API client."""
        self.host = host
        self.token = token

    async def login(self, data: ConfigEntry) -> str:
        """Login to the Grimmory API."""
        _LOGGER.debug(
            "Logging in to Grimmory API at %s as %s",
            data[CONF_HOST],
            data[CONF_USERNAME],
        )

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                f"{data[CONF_HOST]}/api/v1/auth/login",
                json={
                    "username": data[CONF_USERNAME],
                    "password": data[CONF_PASSWORD],
                },
            ) as response,
        ):
            response_json = await response.json()

        _LOGGER.debug(response_json)
        _LOGGER.debug("Login response status: %s", response.status)

        # This only passes if there are no exceptions so it is safe to assume the login was successful after this line.
        response.raise_for_status()

        _LOGGER.debug("Login successful!")

        return response_json["accessToken"]

    async def get_book_count(self):
        """Get the number of books in Grimmory."""

        _LOGGER.debug("Getting book count from Grimmory API at %s", self.host)

        if self.host is None or self.token is None:
            raise RuntimeError("Client is not available")

        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.host}/api/v1/books",
                params={
                    "withDescription": "false",
                    "stripForListView": "true",
                },
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            ) as response,
        ):
            response.raise_for_status()
            books = await response.json()

        _LOGGER.debug("Retrieved %d books from Grimmory API", len(books))

        return len(books)
