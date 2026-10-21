"""Sensor platform for Grimmory."""

import logging

from homeassistant.components.sensor import SensorEntity

from .api import GrimmoryApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up the Grimmory sensor platform."""

    client = entry.runtime_data

    sensors = [
        GrimmorySensor(client),
        # Add more sensors as needed
    ]
    _LOGGER.debug("Setting up Grimmory sensors: %s", sensors)

    async_add_entities(sensors)


class GrimmorySensor(SensorEntity):
    """A test sensor for Grimmory."""

    _attr_name = "Grimmory test"
    _attr_unique_id = "grimmory_test"

    def __init__(self, client: GrimmoryApiClient) -> None:
        """Initialize the sensor."""
        self._client = client
        _LOGGER.debug("GrimmorySensor initialized")

    async def async_update(self) -> None:
        """Fetch number of books."""
        self._attr_native_value = await self._client.get_book_count()
