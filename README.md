# RAV311 Remote — Home Assistant Custom Integration

Control your Yamaha AV receiver from Home Assistant via infrared, using the native [`infrared`](https://www.home-assistant.io/integrations/infrared/) building block introduced in HA 2026.4.

**Compatible models (all use the RAV311 remote):**
- Yamaha RX-V361
- Yamaha RX-V361BL
- Yamaha HTR-6030
- Yamaha HTR-6025

## Requirements

- Home Assistant **2026.4** or later
- An ESPHome device configured with the **IR/RF Proxy** component (infrared transmitter) already added to Home Assistant

## Installation via HACS

1. In HACS, go to **Integrations → Custom repositories**
2. Add this repository URL and select category **Integration**
3. Click **Download**
4. Restart Home Assistant

## Manual installation

Copy the `custom_components/rav311_remote/` folder into your `config/custom_components/` directory, then restart Home Assistant.

## Setup

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **RAV311 Remote**
3. Select the infrared transmitter entity pointed at your receiver
4. Done — your receiver appears as a device with all entities

## Entities created

| Platform | Entity | Notes |
|---|---|---|
| `media_player` | RAV311 Remote | Power, volume, mute, source select |
| `select` | Input Source | CD, DVD, Tuner, V-AUX, XM… |
| `select` | Sound Program | Straight, Enhancer, Surround Decode, Night |
| `button` | Power On / Standby | |
| `button` | Mute, Sleep, Display, Return… | All remote buttons |
| `button` | Program Left/Right | DSP navigation |
| `button` | A-E/Cat, Preset Ch… | Tuner navigation |

All entities use **assumed state** — IR is one-way, so HA tracks the last command sent.

## Protocol notes

The RAV311 remote uses the **Pioneer IR protocol** at 40 kHz.
All codes were sourced from a working ESPHome configuration and verified against the physical remote.
