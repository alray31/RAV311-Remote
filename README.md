# RAV311 Remote — Home Assistant Custom Integration

Control your Yamaha AV receiver from Home Assistant via infrared, using the native [`infrared`](https://www.home-assistant.io/integrations/infrared/) building block introduced in HA 2026.4.

**Compatible models (all use the RAV311 remote):**
- Yamaha RX-V361
- Yamaha RX-V361BL
- Yamaha HTR-6025
- Yamaha HTR-6030

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/e309d791-43ad-4a20-9c49-df5f9dc5df1f" />

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

## Minimum ESPHome hardware setup

1. An ESP32 or ESP6266 MCU
2. An IR diode
3. A transistor
4. A power source

<img width="688" height="586" alt="image" src="https://github.com/user-attachments/assets/23424035-66e3-4836-91f1-823ac231dac7" />

## Minimum ESPHome config

Here is an example of the required esphome config. Change variable to fit your needs (board type, wifi credentials, GPIO, etc)

```
esphome:
  name: irblaster
  friendly_name: IR Blaster

esp8266:
  board: esp01_1m

api:
  encryption:
    key: ""

ota:
  - platform: esphome
    password: ""

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  ap:
    ssid: "IR Blaster Fallback Hotspot"
    password: ""

captive_portal:

remote_transmitter:
  pin: GPIO04
  carrier_duty_percent: 50%
  id: my_ir_transmiter

infrared:
  - platform: ir_rf_proxy
    name: IR Proxy Transmitter Salon
    id: ir_proxy_tx
    remote_transmitter_id: my_ir_transmiter
```

## The original remote this integration replaces. If your remote is like the one in the picture, this integration will work with your AV device.

<img width="353" height="1500" alt="image" src="https://github.com/user-attachments/assets/970544dd-b312-4fa4-8dad-ea983c7817cc" />


