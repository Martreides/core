import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME


class GrimmoryApiClient:
    def __init__(self) -> None:
        """Initialize the Grimmory API client."""

    async def login(self, data: ConfigEntry) -> bool:
        """Login to the Grimmory API."""
        print("Logging in to Grimmory API...")
        print(data[CONF_HOST])
        print(data[CONF_PASSWORD])
        print(data[CONF_USERNAME])

        # TODO Implement login logic

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
            print("Status:", response.status)
            print(await response.text())
            response.raise_for_status()
            print("Login successful!")

        return True
