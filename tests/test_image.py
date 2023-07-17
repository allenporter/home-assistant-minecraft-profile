"""Tests for minecraft profile skin image platform."""

from http import HTTPStatus


import pytest

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.typing import ClientSessionGenerator


@pytest.fixture(name="platforms", autouse=True)
def mock_platforms() -> list[Platform]:
    """Fixture for platforms loaded by the integration."""
    return [Platform.IMAGE]


@pytest.mark.freeze_time("2023-04-01 00:00:00+00:00")
async def test_skin(
    hass: HomeAssistant,
    hass_client: ClientSessionGenerator,
    _setup_api: None,
    _setup_integration: None,
) -> None:
    """Test fetching a profile skin image."""

    state = hass.states.get("image.some_profile_name")
    assert state.state == "2023-04-01T00:00:00+00:00"

    client = await hass_client()
    resp = await client.get("/api/image_proxy/image.some_profile_name")
    assert resp.status == HTTPStatus.OK
    body = await resp.read()
    assert body is not None
