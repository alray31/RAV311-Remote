from __future__ import annotations
from infrared_protocols import Command

PIONEER_FREQUENCY_HZ = 40_000

_HEADER_HIGH = 9000
_HEADER_LOW  = 4500
_BIT_HIGH    = 560
_ONE_LOW     = 1690
_ZERO_LOW    = 560
_TRAILER_HIGH = 560
_TRAILER_LOW  = 25500


def _reverse_bits(b: int) -> int:
    result = 0
    for i in range(8):
        if b & (1 << i):
            result |= (1 << (7 - i))
    return result


def _encode_uint16_lsb(value: int) -> list[int]:
    result = []
    for _ in range(16):
        result.append(_BIT_HIGH)
        result.append(_ONE_LOW if (value & 1) else _ZERO_LOW)
        value >>= 1
    return result


class PioneerCommand(Command):
    """Pioneer IR command matching ESPHome pioneer_protocol.cpp exactly."""

    def __init__(self, rc_code: int, repeat: int = 2) -> None:
        super().__init__(modulation=PIONEER_FREQUENCY_HZ, repeat_count=0)
        self.rc_code = rc_code
        self._repeat = repeat

    def get_raw_timings(self) -> list[int]:
        high_byte = (self.rc_code >> 8) & 0xFF
        low_byte  = self.rc_code & 0xFF
        rev_high  = _reverse_bits(high_byte)
        address   = ((~rev_high & 0xFF) << 8) | rev_high
        command   = ((~low_byte & 0xFF) << 8) | low_byte

        frame: list[int] = [_HEADER_HIGH, _HEADER_LOW]
        frame.extend(_encode_uint16_lsb(address))
        frame.extend(_encode_uint16_lsb(command))
        frame.extend([_TRAILER_HIGH, _TRAILER_LOW])

        timings: list[int] = []
        for _ in range(self._repeat):
            timings.extend(frame)
        return timings
