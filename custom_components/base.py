"""Shared base for all Yamaha Infrared entities."""

from __future__ import annotations

from homeassistant.components import infrared
from homeassistant.core import HomeAssistant

from .const import YamahaCode, make_command

CONF_INFRARED_ENTITY_ID = "infrared_entity_id"


class YamahaIRMixin:
    """Mixin that provides a helper to send Yamaha IR commands."""

    hass: HomeAssistant
    _infrared_entity_id: str

    async def _send(self, code: YamahaCode) -> None:
        """Send a Pioneer-encoded IR command through the infrared building block."""
        await infrared.async_send_command(
            self.hass,
            self._infrared_entity_id,
            make_command(code),
            context=self._context if hasattr(self, "_context") else None,
        )
