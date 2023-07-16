"""Image platform for minecraft profile."""

from __future__ import annotations

import logging
import datetime
from io import BytesIO

from minepi import Player

from homeassistant.components.image import ImageEntity, Image
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import CONF_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


# Player skins don't change that often
SCAN_INTERVAL = datetime.timedelta(hours=24)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the minecraft profile image platform."""
    name = config_entry.data[CONF_NAME]
    player = Player(name=name, session=async_get_clientsession(hass))
    await player.initialize()

    async_add_entities([Skin(hass, player)], True)


class Skin(ImageEntity):
    """Minecraft profile skin."""

    _attr_has_entity_name = True
    _attr_content_type = "image/x-png"
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, player: Player) -> None:
        super().__init__(hass, verify_ssl=False)
        self._player = player
        self._unique_id = player.uuid
        self._attr_name = player.name
        self._attr_device_info = DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name=self._player.name,
        )

    async def async_update(self) -> None:
        """Update the image on poll."""

        # TODO: Handle errors
        await self._player.initialize()

        image = await self._player.skin.render_skin(
            hr=30, vr=0, vrll=10, vrrl=-10, vrla=-10, vrra=10
        )
        buf = BytesIO()
        image.save(buf, format="PNG")
        self._cached_image = Image(
            content_type=self._attr_content_type, content=buf.getbuffer()
        )
        self._attr_image_last_updated = dt_util.utcnow()
