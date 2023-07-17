"""Minecraft profile integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_NAME, CONF_HYPIXEL_API_KEY
from .coordinator import ProfileCoordinator


PLATFORMS: list[Platform] = [Platform.IMAGE, Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    entry.data[CONF_NAME]
    coordinator = ProfileCoordinator(
        hass,
        async_get_clientsession(hass),
        entry.data[CONF_NAME],
        entry.data.get(CONF_HYPIXEL_API_KEY),
    )
    await coordinator.async_config_entry_first_refresh()
    if coordinator.hypixel_coordinator:
        await coordinator.hypixel_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
