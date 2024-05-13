"""Binary sensor platform for minecraft profile."""

from __future__ import annotations

import logging
import datetime


from minepi import Player

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import device_info, HypixelProfileCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


UPDATE_INTERAL = datetime.timedelta(minutes=30)
SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="online",
        name="Hypixel",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        icon="mdi:account-badge",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the minecraft profile image platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    if not coordinator.hypixel_coordinator:
        return

    async_add_entities(
        MinecraftBinarySensor(
            hass=hass,
            player=coordinator.data.player,
            description=description,
            coordinator=coordinator.hypixel_coordinator,
        )
        for description in SENSOR_TYPES
    )


class MinecraftBinarySensor(
    CoordinatorEntity[HypixelProfileCoordinator], BinarySensorEntity
):
    """Minecraft binary sensor entity."""

    entity_description: BinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        player: Player,
        description: BinarySensorEntityDescription,
        coordinator: HypixelProfileCoordinator,
    ) -> None:
        """Initialize MinecraftSensor."""
        super().__init__(coordinator)
        self._player = player
        self.entity_description = description
        self._attr_unique_id = f"{player.uuid}-{description.key}"
        self._attr_device_info = device_info(player)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data.online

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self._handle_coordinator_update()
        await super().async_added_to_hass()
