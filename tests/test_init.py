"""Test for integration init."""
from unittest.mock import patch
import pytest

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.setup import async_setup_component

from custom_components.minecraft_profile.const import CONF_NAME, DOMAIN

from pytest_homeassistant_custom_component.common import MockConfigEntry


@pytest.fixture(name="config_entry")
def mock_config_entry() -> MockConfigEntry:
    """Fixture for mock configuration entry."""
    return MockConfigEntry(domain=DOMAIN, data={})


@pytest.fixture(name="_setup_integration")
async def setup_integration(
    hass: HomeAssistant, config_entry: MockConfigEntry, enable_custom_integrations
) -> None:
    """Set up the integration."""
    _ = enable_custom_integrations
    config_entry.add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()


async def test_init(hass, _setup_integration, config_entry: MockConfigEntry):
    """Test loading the integration."""

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert not hass.data.get(DOMAIN)
    assert config_entry.state is ConfigEntryState.NOT_LOADED