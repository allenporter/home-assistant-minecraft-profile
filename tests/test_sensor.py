"""Tests for minecraft profile sensor platform."""


import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.typing import ClientSessionGenerator


@pytest.fixture(name="platforms", autouse=True)
def mock_platforms() -> list[Platform]:
    """Fixture for platforms loaded by the integration."""
    return [Platform.SENSOR]


@pytest.fixture(name="api_key")
def mock_api_key() -> str | None:
    """Fixture for api key in config entry."""
    return "SOME-API-KEY"


@pytest.mark.freeze_time("2023-04-01 00:00:00+00:00")
async def test_fetch_skin(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    _setup_api: None,
    _setup_hypixel_api: None,
    _setup_integration: None,
) -> None:
    """Test fetching a profile skin image."""

    hass.states.async_entity_ids()

    state = hass.states.get("sensor.self_player_name_hypixel_online")
    assert state.state == "True"

    state = hass.states.get("sensor.self_player_name_hypixel_game_type")
    assert state.state == "some-game-type"

    state = hass.states.get("sensor.self_player_name_hypixel_mode")
    assert state.state == "some-mode"

    state = hass.states.get("sensor.self_player_name_hypixel_map")
    assert state.state == "some-map"
