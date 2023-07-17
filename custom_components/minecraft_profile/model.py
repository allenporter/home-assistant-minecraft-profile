"""Data update coorindator for minecraft profile."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from minepi import Player


_LOGGER = logging.getLogger(__name__)


@dataclass
class Profile:
    """Profile information about a player."""

    player: Player
    """Information from the Minecraft API about a player."""


@dataclass
class HypixelSession:
    """A players Hypixel session information."""

    online: bool
    game_type: str
    map: str
