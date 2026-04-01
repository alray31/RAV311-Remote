"""Media player entity for RAV311 Remote via infrared."""

from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base import YamahaIRMixin, CONF_INFRARED_ENTITY_ID
from .const import YamahaCode

DOMAIN = "rav311_remote"

SUPPORTED_FEATURES = (
    MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
)

INPUT_SOURCES = {
    "CD": YamahaCode.CD,
    "MD/CD-R": YamahaCode.MD_CDR,
    "Tuner": YamahaCode.TUNER,
    "DVD": YamahaCode.DVD,
    "DVT/CBL": YamahaCode.DVT_CBL,
    "DVR": YamahaCode.DVR,
    "V-AUX": YamahaCode.V_AUX,
    "XM": YamahaCode.XM,
    "Multi CH IN": YamahaCode.MULTI_CH_IN,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Yamaha media player."""
    async_add_entities(
        [RAV311RemoteMediaPlayer(entry)],
        update_before_add=True,
    )


class RAV311RemoteMediaPlayer(YamahaIRMixin, MediaPlayerEntity):
    """RAV311 Remote media player (assumed state, infrared).

    Compatible with: Yamaha RX-V361, RX-V361BL, HTR-6030, HTR-6025.
    """

    _attr_has_entity_name = True
    _attr_name = None  # uses device name
    _attr_supported_features = SUPPORTED_FEATURES
    _attr_source_list = list(INPUT_SOURCES.keys())

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._infrared_entity_id: str = entry.data[CONF_INFRARED_ENTITY_ID]
        self._attr_unique_id = f"{entry.entry_id}_media_player"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "RAV311 Remote",
            "manufacturer": "Yamaha",
            "model": "RX-V361 / RX-V361BL / HTR-6030 / HTR-6025",
        }
        # Assumed state — starts unknown
        self._attr_state = MediaPlayerState.OFF
        self._attr_is_volume_muted = False
        self._attr_source = None

    @property
    def assumed_state(self) -> bool:
        return True

    async def async_turn_on(self) -> None:
        await self._send(YamahaCode.POWER_ON)
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        await self._send(YamahaCode.STANDBY)
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    async def async_volume_up(self) -> None:
        await self._send(YamahaCode.VOLUME_UP)

    async def async_volume_down(self) -> None:
        await self._send(YamahaCode.VOLUME_DOWN)

    async def async_mute_volume(self, mute: bool) -> None:
        await self._send(YamahaCode.MUTE)
        self._attr_is_volume_muted = not self._attr_is_volume_muted
        self.async_write_ha_state()

    async def async_select_source(self, source: str) -> None:
        if code := INPUT_SOURCES.get(source):
            await self._send(code)
            self._attr_source = source
            self.async_write_ha_state()
