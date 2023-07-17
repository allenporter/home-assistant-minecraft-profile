"""Image platform for minecraft profile."""

from __future__ import annotations

import logging
import datetime
from io import BytesIO


from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN
from .coordinator import ProfileCoordinator, device_info
from .model import Profile

_LOGGER = logging.getLogger(__name__)


# Player skins don't change that often
SCAN_INTERVAL = datetime.timedelta(hours=24)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the minecraft profile image platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([Skin(hass, coordinator)], True)


class Skin(CoordinatorEntity[Profile], ImageEntity):
    """Minecraft profile skin."""

    _attr_has_entity_name = True
    _attr_content_type = "image/x-png"
    _attr_icon = "mdi:minecraft"

    def __init__(self, hass: HomeAssistant, coordinator: ProfileCoordinator) -> None:
        super().__init__(coordinator)
        ImageEntity.__init__(self, hass, verify_ssl=False)
        self._attr_unique_id = coordinator.data.player.uuid
        self._attr_name = None
        self._attr_device_info = device_info(coordinator.data.player)
        self._attr_image_last_updated = dt_util.utcnow()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_image_last_updated = dt_util.utcnow()
        self.async_write_ha_state()

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        player = self.coordinator.data.player
        image = await player.skin.render_skin(
            hr=30, vr=0, vrll=10, vrrl=-10, vrla=-10, vrra=10
        )
        buf = BytesIO()
        image.save(buf, format="PNG")
        return buf.getbuffer()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self._handle_coordinator_update()
        await super().async_added_to_hass()
