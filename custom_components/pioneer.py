"""Pioneer IR protocol encoder.

Encodes Pioneer RC codes into raw microsecond timings compatible with
the Home Assistant infrared building block (InfraredCommand).

The Pioneer protocol is NEC-based:
- 40 kHz carrier
- 9000 µs header mark + 4500 µs header space
- Bit 1: 560 µs mark + 1690 µs space
- Bit 0: 560 µs mark + 560 µs space
- 560 µs trailing mark
- For repeat=2, a 40 ms gap then the full frame is resent.
"""

from __future__ import annotations

from dataclasses import dataclass

PIONEER_FREQUENCY_HZ = 40_000  # 40 kHz carrier

_HEADER_MARK = 9000
_HEADER_SPACE = 4500
_BIT_MARK = 560
_ONE_SPACE = 1690
_ZERO_SPACE = 560
_TRAILING_MARK = 560
_REPEAT_GAP = 40_000  # µs gap between repetitions


def _encode_byte(byte: int) -> list[int]:
    """Return mark/space pairs for 8 bits, LSB first."""
    timings: list[int] = []
    for i in range(8):
        bit = (byte >> i) & 1
        timings.append(_BIT_MARK)
        timings.append(_ONE_SPACE if bit else _ZERO_SPACE)
    return timings


def _encode_frame(rc_code: int) -> list[int]:
    """Encode a 16-bit Pioneer RC code as one full frame."""
    high_byte = (rc_code >> 8) & 0xFF
    low_byte = rc_code & 0xFF

    timings: list[int] = [_HEADER_MARK, _HEADER_SPACE]
    timings.extend(_encode_byte(high_byte))
    timings.extend(_encode_byte(~high_byte & 0xFF))  # inverted byte
    timings.extend(_encode_byte(low_byte))
    timings.extend(_encode_byte(~low_byte & 0xFF))   # inverted byte
    timings.append(_TRAILING_MARK)
    return timings


@dataclass
class PioneerCommand:
    """An IR command encoded using the Pioneer protocol."""

    rc_code: int
    repeat: int = 2

    def get_modulation(self) -> int:
        """Return carrier frequency in Hz."""
        return PIONEER_FREQUENCY_HZ

    def get_raw_timings(self) -> list[int]:
        """Return raw alternating mark/space timings in microseconds.

        Positive values = mark (LED on), no sign convention needed here;
        the InfraredEntity implementation handles conversion to the
        hardware-specific format.
        """
        frame = _encode_frame(self.rc_code)
        timings = list(frame)
        for _ in range(self.repeat - 1):
            timings.append(_REPEAT_GAP)
            timings.extend(frame)
        return timings
