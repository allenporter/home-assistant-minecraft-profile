"""Config flow for the Minecraft Profile integration."""

from homeassistant import config_entries
from .const import DOMAIN


class MinecraftProfileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
