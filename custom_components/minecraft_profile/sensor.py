"""Sensor platform for minecraft profile."""

from __future__ import annotations

import logging
import datetime
import dataclasses

from minepi import Player

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import ProfileCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


UPDATE_INTERAL = datetime.timedelta(minutes=30)
API_KEY_HEADER = "API-Key"
TIMEOUT = 10.0
PLAYER_API = "https://api.hypixel.net/player"


SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="online", name="Hypixel Online", icon="mdi:account-badge"
    ),
    SensorEntityDescription(
        key="game_type",
        name="Hypixel game type",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:controller-classic",
    ),
    SensorEntityDescription(
        key="mode",
        name="Hypixel mode",
        entity_category=EntityCategory.DIAGNOSTIC,
        # XXX icon
    ),
    SensorEntityDescription(
        key="map",
        name="Hypixel map",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:map",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the minecraft profile image platform."""
    # TODOs:
    # Create coordinated entity to pull in data
    # Setup polling: Separate coordinator? Same coordinator?

    # name = config_entry.data[CONF_NAME]
    # hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    if not coordinator.hypixel_coordinator:
        return

    async_add_entities(
        MinecraftSensor(
            hass=hass,
            player=coordinator.data.player,
            description=description,
            coordinator=coordinator.hypixel_coordinator,
        )
        for description in SENSOR_TYPES
    )


class MinecraftSensor(CoordinatorEntity[ProfileCoordinator], SensorEntity):
    """Minecraft sensor entity."""

    entity_description: SensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        player: Player,
        description: SensorEntityDescription,
        coordinator: ProfileCoordinator,
    ) -> None:
        """Initialize MinecraftSensor."""
        super().__init__(coordinator)
        self._player = player
        self.entity_description = description
        self._attr_unique_id = f"{player.uuid}-{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, player.uuid)
            },
            name="{self._player.name}",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = dataclasses.asdict(self.coordinator.data)
        self._attr_native_value = data[self.entity_description.key]
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self._handle_coordinator_update()
        await super().async_added_to_hass()
