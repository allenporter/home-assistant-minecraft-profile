"""Fixtures for tests."""

from collections.abc import Generator
from urllib.request import urlopen
from unittest.mock import patch

import pytest

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.minecraft_profile.const import (
    DOMAIN,
    CONF_NAME,
    CONF_HYPIXEL_API_KEY,
)

from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker


PROFILE_NAME = "some-profile-name"
PROFILE_ID = "a6b14651eea643aa900fdf619d4b02da"
NAME_TO_ID = {"name": PROFILE_NAME, "id": PROFILE_ID}
UID_TO_PROFIE = {
    "id": PROFILE_ID,
    "name": PROFILE_NAME,
    "properties": [
        {
            "name": "textures",
            "value": "ewogICJ0aW1lc3RhbXAiIDogMTY4OTQ3NzA4NDI3MiwKICAicHJvZmlsZUlkIiA6ICJhNmIxNDY1MWVlYTY0M2FhOTAwZmRmNjE5ZDRiMDJkYSIsCiAgInByb2ZpbGVOYW1lIiA6ICJzdGFtcHlsb25nbm9zZSIsCiAgInRleHR1cmVzIiA6IHsKICAgICJTS0lOIiA6IHsKICAgICAgInVybCIgOiAiaHR0cDovL3RleHR1cmVzLm1pbmVjcmFmdC5uZXQvdGV4dHVyZS9lYjMxMmI4ZDZkMWYyOWIyMDUyNWFiNzNiODM3N2UxMGI0Mjc5ODYzOTgwZWE2MjQ1OTcwZTBjNzBmZDEzYzNhIgogICAgfQogIH0KfQ==",  # noqa: E501
        }
    ],
    "profileActions": {},
}
SKIN_URL = "http://textures.minecraft.net/texture/eb312b8d6d1f29b20525ab73b8377e10b4279863980ea6245970e0c70fd13c3a"  # noqa: E501
DATA_URI = "data:image/png;base64,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"  # noqa: E501
HYPIXEL_STATUS = {
    "success": True,
    "uuid": PROFILE_ID,
    "session": {
        "online": True,
        "gameType": "SKYWARS",
        "map": "some-map",
    },
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """Enable custom integration."""
    _ = enable_custom_integrations  # unused
    yield


@pytest.fixture(name="_setup_api")
def mock_api(
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Fixture to construct a fake calendar list API response."""
    aioclient_mock.get(
        f"https://api.mojang.com/users/profiles/minecraft/{PROFILE_NAME}",
        json=NAME_TO_ID,
    )
    aioclient_mock.get(
        f"https://sessionserver.mojang.com/session/minecraft/profile/{PROFILE_ID}",
        json=UID_TO_PROFIE,
    )
    with urlopen(DATA_URI) as response:
        data = response.read()
        aioclient_mock.get(
            SKIN_URL,
            content=data,
        )


@pytest.fixture(name="api_key")
def mock_api_key() -> str | None:
    """Fixture for api key in config entry."""
    return None


@pytest.fixture(name="_setup_hypixel_api")
def mock_hypixel_api(
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Fixture to construct a fake calendar list API response."""
    aioclient_mock.get(
        "https://api.hypixel.net/status",
        json=HYPIXEL_STATUS,
    )


@pytest.fixture(name="config_entry")
def mock_config_entry(api_key: str) -> MockConfigEntry:
    """Fixture for mock configuration entry."""
    data = {CONF_NAME: PROFILE_NAME}
    if api_key:
        data[CONF_HYPIXEL_API_KEY] = api_key
    return MockConfigEntry(domain=DOMAIN, data=data)


@pytest.fixture(name="platforms")
def mock_platforms() -> list[Platform]:
    """Fixture for platforms loaded by the integration."""
    return []


@pytest.fixture(name="_setup_integration")
async def setup_integration(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    platforms: list[Platform],
) -> None:
    """Set up the integration."""
    config_entry.add_to_hass(hass)
    with patch("custom_components.minecraft_profile.PLATFORMS", platforms):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
