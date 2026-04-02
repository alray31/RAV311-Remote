"""RAV311 Remote IR codes and command factory.

Compatible with Yamaha RX-V361, RX-V361BL, HTR-6030, HTR-6025.
"""
from __future__ import annotations

from enum import IntEnum

from .pioneer import PioneerCommand


class YamahaCode(IntEnum):
    """IR codes for receivers using the Yamaha RAV311 remote."""

    POWER_ON = 0x7E7E
    STANDBY = 0x7E7F
    VOLUME_UP = 0x5E1A
    VOLUME_DOWN = 0x5E1B
    MUTE = 0x5E1C
    SLEEP = 0x5E57
    AUDIO_SELECT = 0x5EC3
    MULTI_CH_IN = 0x5E87
    LEVEL = 0x
