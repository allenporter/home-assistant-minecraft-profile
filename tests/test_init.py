"""Test for integration init."""
from typing import Any

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from custom_components.minecraft_profile.const import DOMAIN

from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_init(
    hass: HomeAssistant,
    _setup_api: None,
    _setup_integration: Any,
    config_entry: MockConfigEntry,
) -> None:
    """Test loading the integration."""

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert not hass.data.get(DOMAIN)
    assert config_entry.state is ConfigEntryState.NOT_LOADED
