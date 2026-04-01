"""Select entities for RAV311 Remote — input source and sound program."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base import YamahaIRMixin, CONF_INFRARED_ENTITY_ID
from .const import YamahaCode, INPUT_SOURCES, SOUND_PROGRAMS

DOMAIN = "rav311_remote"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""
    infrared_entity_id: str = entry.data[CONF_INFRARED_ENTITY_ID]
    async_add_entities([
        YamahaInputSelect(entry, infrared_entity_id),
        YamahaSoundProgramSelect(entry, infrared_entity_id),
    ])


class YamahaInputSelect(YamahaIRMixin, SelectEntity):
    """Select entity to switch input source."""

    _attr_has_entity_name = True
    _attr_name = "Input Source"
    _attr_options = list(INPUT_SOURCES.keys())

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_input_source"
        self._attr_current_option = None  # assumed state
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "RAV311 Remote",
            "manufacturer": "Yamaha",
            "model": "RX-V361 / RX-V361BL / HTR-6030 / HTR-6025",
        }

    @property
    def assumed_state(self) -> bool:
        return True

    async def async_select_option(self, option: str) -> None:
        if code := INPUT_SOURCES.get(option):
            await self._send(code)
            self._attr_current_option = option
            self.async_write_ha_state()


class YamahaSoundProgramSelect(YamahaIRMixin, SelectEntity):
    """Select entity to choose sound program."""

    _attr_has_entity_name = True
    _attr_name = "Sound Program"
    _attr_options = list(SOUND_PROGRAMS.keys())
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry: ConfigEntry, infrared_entity_id: str) -> None:
        self._infrared_entity_id = infrared_entity_id
        self._attr_unique_id = f"{entry.entry_id}_sound_program"
        self._attr_current_option = None
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "RAV311 Remote",
            "manufacturer": "Yamaha",
            "model": "RX-V361 / RX-V361BL / HTR-6030 / HTR-6025",
        }

    @property
    def assumed_state(self) -> bool:
        return True

    async def async_select_option(self, option: str) -> None:
        if code := SOUND_PROGRAMS.get(option):
            await self._send(code)
            self._attr_current_option = option
            self.async_write_ha_state()
