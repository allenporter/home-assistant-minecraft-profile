"""Tests for minecraft profile sensor platform."""


import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.typing import ClientSessionGenerator


@pytest.fixture(name="platforms", autouse=True)
def mock_platforms() -> list[Platform]:
    """Fixture for platforms loaded by the integration."""
    return [Platform.BINARY_SENSOR]


@pytest.fixture(name="api_key")
def mock_api_key() -> str | None:
    """Fixture for api key in config entry."""
    return "SOME-API-KEY"


async def test_binary_sensor(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    _setup_api: None,
    _setup_hypixel_api: None,
    _setup_integration: None,
) -> None:
    """Test binary sensor values."""

    state = hass.states.get("binary_sensor.some_profile_name_hypixel")
    assert state.state == "on"
