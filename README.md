![banner](https://raw.githubusercontent.com/alray31/RAV311-Remote/main/assets/banner.gif)

# RAV311 Remote — Home Assistant Custom Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration) [![HACS Validation](https://github.com/alray31/RAV311-Remote/actions/workflows/hacs.yml/badge.svg)](https://github.com/alray31/RAV311-Remote/actions/workflows/hacs.yml) [![Hassfest](https://github.com/alray31/RAV311-Remote/actions/workflows/hassfest.yml/badge.svg)](https://github.com/alray31/RAV311-Remote/actions/workflows/hassfest.yml) [![GitHub Release](https://img.shields.io/github/v/release/alray31/RAV311-Remote?style=flat&color=orange)](https://github.com/alray31/RAV311-Remote/releases) [![GitHub Release Date](https://img.shields.io/github/release-date/alray31/RAV311-Remote)](https://github.com/alray31/RAV311-Remote/releases) [![GitHub Stars](https://img.shields.io/github/stars/alray31/RAV311-Remote?style=flat)](https://github.com/alray31/RAV311-Remote/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/alray31/RAV311-Remote?style=flat)](https://github.com/alray31/RAV311-Remote/network/members) [![GitHub Issues](https://img.shields.io/github/issues/alray31/RAV311-Remote)](https://github.com/alray31/RAV311-Remote/issues) [![Last Commit](https://img.shields.io/github/last-commit/alray31/RAV311-Remote)](https://github.com/alray31/RAV311-Remote/commits) [![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.4%2B-41BDF5?logo=homeassistant)](https://www.home-assistant.io/) [![License](https://img.shields.io/github/license/alray31/RAV311-Remote)](LICENSE)

Control your Yamaha AV receiver from Home Assistant via infrared, using the native [`infrared`](https://www.home-assistant.io/integrations/infrared/) building block introduced in HA 2026.4.

**Compatible models (all use the RAV311 remote):**
- Yamaha RX-V361
- Yamaha RX-V361BL
- Yamaha HTR-6025
- Yamaha HTR-6030
- Maybe more, you tell me!


## Requirements

- Home Assistant **2026.4** or later
- An ESPHome device configured with the **IR/RF Proxy** component (infrared transmitter) already added to Home Assistant

## Installation via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=RAV311-Remote&owner=alray31)

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

Here is an example of the required esphome config. Change variables to fit your needs (board type, wifi credentials, GPIO, etc)
1. You need to add the [ir transmitter](https://esphome.io/components/remote_transmitter/) component, set the correct GPIO corresponding to the IR LED and give your ir tranmisster an ID.
2. Then add the [ir proxy](https://esphome.io/components/ir_rf_proxy/) transmitter compoenent, set the "remote_transmitter_id:" value so it matches the ID previously give the the ir_transmitter.

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

## The original remote this integration replaces. 

If your remote or AV receiver looks like this, this integration will control your AV device.

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/e309d791-43ad-4a20-9c49-df5f9dc5df1f" />

<img width="353" height="1500" alt="image" src="https://github.com/user-attachments/assets/970544dd-b312-4fa4-8dad-ea983c7817cc" />



