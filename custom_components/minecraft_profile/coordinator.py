"""Data update coorindator for minecraft profile."""

from __future__ import annotations

import logging
import datetime
from http import HTTPStatus
from typing import Any

import aiohttp
import async_timeout
from aiohttp.client_exceptions import (
    ClientError,
    ClientResponseError,
)
from minepi import Player

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .model import Profile, HypixelSession
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


UPDATE_INTERAL = datetime.timedelta(minutes=30)
API_KEY_HEADER = "API-Key"
TIMEOUT = 10.0
STATUS_API = "https://api.hypixel.net/status"
UUID = "uuid"


def device_info(player: Player) -> DeviceInfo:
    """Create DeviceInfo for a player."""
    return DeviceInfo(
        identifiers={(DOMAIN, player.uuid)},
        name=f"{player.name}",
    )


class ProfileCoordinator(DataUpdateCoordinator[Profile]):
    """Minecraft Profile coordinator."""

    data: Profile

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        name: str,
        api_key: str | None,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Minecraft Profile",
            update_interval=UPDATE_INTERAL,
        )
        self._session = session
        self._player = Player(name=name, session=async_get_clientsession(hass))
        self._name = name
        self._hypixel_coordinator: HypixelProfileCoordinator | None = None
        if api_key:
            self._hypixel_coordinator = HypixelProfileCoordinator(
                self.hass, self._session, self._player, api_key
            )

    async def _async_update_data(self) -> Profile:
        """Fetch data from API endpoint."""
        await self._player.initialize()
        return Profile(player=self._player)

    @property
    def hypixel_coordinator(self) -> HypixelProfileCoordinator | None:
        """Create a HypixelProfileCoordinator."""
        return self._hypixel_coordinator


class HypixelProfileCoordinator(DataUpdateCoordinator[HypixelSession]):
    """Minecraft Hypixel profile coordinator."""

    data: HypixelSession

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        player: Player,
        api_key: str | None,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Minecraft Profile",
            update_interval=UPDATE_INTERAL,
        )
        self._session = session
        self._player = player
        if api_key:
            self._headers = {API_KEY_HEADER: api_key}
        else:
            self._headers: dict[str, str] = {}

    async def _async_update_data(self) -> HypixelSession:
        """Fetch data from API endpoint."""
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(TIMEOUT):
                response = await self._session.get(
                    STATUS_API,
                    headers=self._headers,
                    params={UUID: self._player.uuid},
                )
                result: dict[str, Any] = await response.json()
        except ClientResponseError as err:
            if err.status == HTTPStatus.FORBIDDEN:
                raise ConfigEntryAuthFailed from err
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        if not result.get("success", False):
            raise UpdateFailed(f"Error response from API: {result}")
        _LOGGER.debug("Hypixel response: %s", result)
        session = result.get("session", {})
        return HypixelSession(
            online=session.get("online", False),
            game_type=session.get("gameType", "UNKNOWN").lower(),
            map=session.get("map", ""),
        )
