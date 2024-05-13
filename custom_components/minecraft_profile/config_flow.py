"""Config flow for the Minecraft Profile integration."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_NAME, CONF_HYPIXEL_API_KEY


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Optional(CONF_HYPIXEL_API_KEY): str,
    }
)


class MinecraftProfileConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
