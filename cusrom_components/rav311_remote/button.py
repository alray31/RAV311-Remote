"""Button entities for RAV311 Remote — one per IR command."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base import YamahaIRMixin, CONF_INFRARED_ENTITY_ID
from .const import YamahaCode, YAMAHA_CODE_LABELS

DOMAIN = "rav311_remote"

# Buttons that belong to the config entity_category (not shown on default dashboard)
_CONFIG_BUTTONS = {
    YamahaCode.SLEEP,
    YamahaCode.AUDIO_SELECT,
    YamahaCode.LEVEL,
    YamahaCode.DISPLAY,
    YamahaCode.RETURN,
    YamahaCode.SEARCH_MENU,
    YamahaCode.PRESET_CH_UP,
    YamahaCode.PRESET_CH_DOWN,
    YamahaCode.AE_CAT_RIGHT,
    YamahaCode.AE_CAT_LEFT,
    YamahaCode.PROGRAM_LEFT,
    YamahaCode.PROGRAM_RIGHT,
    YamahaCode.NUM_8,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up one button per Yamaha IR command."""
    infrared_entity_id: str = entry.data[CONF_INFRARED_ENTITY_ID]

    buttons = [
        YamahaButton(entry, code, label, infrared_entity_id)
        for code, label in YAMAHA_CODE_LABELS.items()
    ]
    async_add_entities(buttons)


class YamahaButton(YamahaIRMixin, ButtonEntity):
    """A button that fires one Yamaha IR command."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        code: YamahaCode,
        label: str,
        infrared_entity_id: str,
    ) -> None:
        self._code = code
        self._infrared_entity_id = infrared_entity_id
        self._attr_name = label
        self._attr_unique_id = f"{entry.entry_id}_btn_{code.name.lower()}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "RAV311 Remote",
            "manufacturer": "Yamaha",
            "model": "RX-V361 / RX-V361BL / HTR-6030 / HTR-6025",
        }
        if code in _CONFIG_BUTTONS:
            from homeassistant.const import EntityCategory
            self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        """Send the IR command."""
        await self._send(self._code)
