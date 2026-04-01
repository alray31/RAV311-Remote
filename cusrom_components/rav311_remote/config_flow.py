"""Config flow for RAV311 Remote."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components import infrared
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er

DOMAIN = "rav311_remote"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"


class RAV311RemoteConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Yamaha Infrared."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Gather available infrared emitter entities
        emitter_entity_ids: list[str] = infrared.async_get_emitters(self.hass)

        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        # Build a friendly label → entity_id map for the dropdown
        ent_reg = er.async_get(self.hass)
        emitter_options: dict[str, str] = {}
        for entity_id in emitter_entity_ids:
            entry = ent_reg.async_get(entity_id)
            label = (
                entry.name or entry.original_name or entity_id
                if entry
                else entity_id
            )
            emitter_options[entity_id] = label

        if user_input is not None:
            selected = user_input[CONF_INFRARED_ENTITY_ID]

            # Prevent duplicate entries for the same emitter
            await self.async_set_unique_id(f"rav311_remote_{selected}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"RAV311 Remote ({emitter_options.get(selected, selected)})",
                data={CONF_INFRARED_ENTITY_ID: selected},
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_INFRARED_ENTITY_ID): vol.In(emitter_options),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
