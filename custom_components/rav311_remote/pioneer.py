from __future__ import annotations
from dataclasses import dataclass

PIONEER_FREQUENCY_HZ = 40_000

_HEADER_HIGH_US = 9000
_HEADER_LOW_US = 4500
_BIT_HIGH_US = 560
_BIT_ONE_LOW_US = 1690
_BIT_ZERO_LOW_US = 560
_TRAILER_HIGH_US = 560
_TRAILER_SPACE_US = 25500


@dataclass
class Timing:
    high_us: int
    low_us: int


def _encode_uint16_lsb(dst: list[Timing], value: int) -> None:
    """Encode 16 bits LSB first, comme NEC/Pioneer."""
    for _ in range(16):
        if value & 1:
            dst.append(Timing(_BIT_HIGH_US, _BIT_ONE_LOW_US))
        else:
            dst.append(Timing(_BIT_HIGH_US, _BIT_ZERO_LOW_US))
        value >>= 1


def _encode_nec_frame(dst: list[Timing], address: int, command: int) -> None:
    """Encode une trame NEC complète (address 16 bits + command 16 bits)."""
    dst.append(Timing(_HEADER_HIGH_US, _HEADER_LOW_US))
    _encode_uint16_lsb(dst, address)
    _encode_uint16_lsb(dst, command)
    dst.append(Timing(_TRAILER_HIGH_US, _TRAILER_SPACE_US))


def _pioneer_to_nec(rc_code: int) -> tuple[int, int]:
    """
    Convertit un rc_code Pioneer 16 bits en (address, command) NEC,
    en suivant exactement pioneer_protocol.cpp d'ESPHome.

    address = (rc_code & 0xff00) | (~(rc_code >> 8) & 0xff)
    command = inversion bit par bit des 4 bits bas → octet haut,
              puis complémenté pour l'octet bas
    """
    address = (rc_code & 0xFF00) | ((~(rc_code >> 8)) & 0xFF)

    # Reconstruction du command : les 4 bits bas de rc_code,
    # inversés en position (bit 0→7, 1→6, 2→5, 3→4)
    cmd_high = 0
    for bit in range(4):
        if (rc_code >> bit) & 1:
            cmd_high |= (1 << (7 - bit))
    # L'octet bas du command est le complément de l'octet haut
    command = (cmd_high << 8) | ((~cmd_high) & 0xFF)

    return address, command


@dataclass
class PioneerCommand:
    rc_code: int
    repeat: int = 2

    @property
    def modulation(self) -> int:
        return PIONEER_FREQUENCY_HZ

    def get_raw_timings(self) -> list[Timing]:
        address, command = _pioneer_to_nec(self.rc_code)
        timings: list[Timing] = []
        for _ in range(self.repeat):
            _encode_nec_frame(timings, address, command)
        return timings
