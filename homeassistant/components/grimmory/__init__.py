"""The grimmory integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant

from .api import GrimmoryApiClient

_PLATFORMS: list[Platform] = [Platform.SENSOR]

type GrimmoryConfigEntry = ConfigEntry[GrimmoryApiClient]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: GrimmoryConfigEntry) -> bool:
    """Set up grimmory from a config entry."""

    client = GrimmoryApiClient(entry.data[CONF_HOST], entry.data[CONF_TOKEN])

    entry.runtime_data = client
    _LOGGER.debug("Grimmory API client initialized")
    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: GrimmoryConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, _PLATFORMS)
