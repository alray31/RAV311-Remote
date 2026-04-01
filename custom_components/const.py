"""RAV311 Remote IR codes and command factory.

Compatible with Yamaha RX-V361, RX-V361BL, HTR-6030, HTR-6025.

All codes use the Pioneer protocol with repeat=2, exactly matching
the ESPHome remote_transmitter.transmit_pioneer configuration.
"""

from __future__ import annotations

from enum import IntEnum

from .pioneer import PioneerCommand

REPEAT = 2


class YamahaCode(IntEnum):
    """IR codes for receivers using the Yamaha RAV311 remote."""

    # Power
    POWER_ON = 0x7E7E
    STANDBY = 0x7E7F

    # Volume
    VOLUME_UP = 0x5E1A
    VOLUME_DOWN = 0x5E1B
    MUTE = 0x5E1C

    # Misc
    SLEEP = 0x5E57
    AUDIO_SELECT = 0x5EC3
    MULTI_CH_IN = 0x5E87
    LEVEL = 0x5E86
    DISPLAY = 0x5EC2
    RETURN = 0x5EAA

    # Input sources
    CD = 0x5E15
    MD_CDR = 0x5EC9
    TUNER = 0x5E16
    DVD = 0x5EC1
    DVT_CBL = 0x5E54
    DVR = 0x5E13
    V_AUX = 0x5E55
    XM = 0x5EB4

    # Navigation / Search
    SEARCH_MENU = 0x5E84
    PRESET_CH_UP = 0x5E9D
    PRESET_CH_DOWN = 0x5E9C
    AE_CAT_RIGHT = 0x5E9E
    AE_CAT_LEFT = 0x5E9F

    # DSP / Sound modes
    PROGRAM_LEFT = 0x5E59
    PROGRAM_RIGHT = 0x5E58
    ENHANCER = 0x5E94
    STRAIGHT = 0x5E56
    SURROUND_DECODE = 0x5E8D
    NIGHT = 0x5E95

    # Numeric (only 8 was present in the ESPHome config)
    NUM_8 = 0x5EDD


# Human-readable labels for each code (used in button entities)
YAMAHA_CODE_LABELS: dict[YamahaCode, str] = {
    YamahaCode.POWER_ON: "Power On",
    YamahaCode.STANDBY: "Standby",
    YamahaCode.VOLUME_UP: "Volume Up",
    YamahaCode.VOLUME_DOWN: "Volume Down",
    YamahaCode.MUTE: "Mute",
    YamahaCode.SLEEP: "Sleep",
    YamahaCode.AUDIO_SELECT: "Audio Select",
    YamahaCode.MULTI_CH_IN: "Multi CH IN",
    YamahaCode.LEVEL: "Level",
    YamahaCode.DISPLAY: "Display",
    YamahaCode.RETURN: "Return",
    YamahaCode.CD: "CD",
    YamahaCode.MD_CDR: "MD/CD-R",
    YamahaCode.TUNER: "Tuner",
    YamahaCode.DVD: "DVD",
    YamahaCode.DVT_CBL: "DVT/CBL",
    YamahaCode.DVR: "DVR",
    YamahaCode.V_AUX: "V-AUX",
    YamahaCode.XM: "XM",
    YamahaCode.SEARCH_MENU: "Search/Menu",
    YamahaCode.PRESET_CH_UP: "Preset/Ch Up",
    YamahaCode.PRESET_CH_DOWN: "Preset/Ch Down",
    YamahaCode.AE_CAT_RIGHT: "A-E/Cat Right",
    YamahaCode.AE_CAT_LEFT: "A-E/Cat Left",
    YamahaCode.PROGRAM_LEFT: "Program Left",
    YamahaCode.PROGRAM_RIGHT: "Program Right",
    YamahaCode.ENHANCER: "Enhancer",
    YamahaCode.STRAIGHT: "Straight",
    YamahaCode.SURROUND_DECODE: "Surround Decode",
    YamahaCode.NIGHT: "Night",
    YamahaCode.NUM_8: "8",
}

# Input sources available for the select entity
INPUT_SOURCES: dict[str, YamahaCode] = {
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

# Sound programs for the select entity
SOUND_PROGRAMS: dict[str, YamahaCode] = {
    "Straight": YamahaCode.STRAIGHT,
    "Enhancer": YamahaCode.ENHANCER,
    "Surround Decode": YamahaCode.SURROUND_DECODE,
    "Night": YamahaCode.NIGHT,
}


def make_command(code: YamahaCode) -> PioneerCommand:
    """Create a PioneerCommand for the given Yamaha code."""
    return PioneerCommand(rc_code=int(code), repeat=REPEAT)
