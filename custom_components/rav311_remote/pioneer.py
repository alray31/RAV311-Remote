from __future__ import annotations
from dataclasses import dataclass

PIONEER_FREQUENCY_HZ = 40_000

_HEADER_MARK = 9000
_HEADER_SPACE = 4500
_BIT_MARK = 560
_ONE_SPACE = 1690
_ZERO_SPACE = 560
_TRAILING_MARK = 560
_REPEAT_GAP = 40_000


@dataclass
class Timing:
    """A single mark/space pair as expected by InfraredCommand.get_raw_timings()."""
    high_us: int
    low_us: int


def _encode_byte(byte: int) -> list[Timing]:
    timings: list[Timing] = []
    for i in range(8):
        bit = (byte >> i) & 1
        timings.append(Timing(high_us=_BIT_MARK, low_us=_ONE_SPACE if bit else _ZERO_SPACE))
    return timings


def _encode_frame(rc_code: int) -> list[Timing]:
    high_byte = (rc_code >> 8) & 0xFF
    low_byte = rc_code & 0xFF

    timings: list[Timing] = [Timing(high_us=_HEADER_MARK, low_us=_HEADER_SPACE)]
    timings.extend(_encode_byte(high_byte))
    timings.extend(_encode_byte(~high_byte & 0xFF))
    timings.extend(_encode_byte(low_byte))
    timings.extend(_encode_byte(~low_byte & 0xFF))
    # Trailing mark — low_us=0 car c'est la fin de trame
    timings.append(Timing(high_us=_TRAILING_MARK, low_us=0))
    return timings


@dataclass
class PioneerCommand:
    """IR command encodé en Pioneer, compatible avec InfraredCommand."""

    rc_code: int
    repeat: int = 2

    @property
    def modulation(self) -> int:
        return PIONEER_FREQUENCY_HZ

    def get_raw_timings(self) -> list[Timing]:
        frame = _encode_frame(self.rc_code)
        timings = list(frame)
        for _ in range(self.repeat - 1):
            # Gap entre répétitions — on l'encode comme un Timing avec high=0
            timings.append(Timing(high_us=0, low_us=_REPEAT_GAP))
            timings.extend(frame)
        return timings
