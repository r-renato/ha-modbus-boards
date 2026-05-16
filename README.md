# DRP Modbus Boards — Home Assistant Custom Integration

A Home Assistant custom integration that bridges **Modbus RTU/TCP boards** to native HA entities (sensors, binary sensors, switches, numbers). Configuration is YAML-driven; the UI is used only to register the integration and show its status.

---

## Supported Boards

| Board identifier | Description |
|---|---|
| `eletechsup_n4dba06` | 8-ch Analog/Digital IO (ADC + DAC, 0–10 V / 0–20 mA) |
| `eletechsup_n4rod08` | 8-ch RS-485 Modbus RTU relay |
| `eletechsup_r4d3b16` | 16-ch relay board |
| `eletechsup_10ioa04` | 4-ch analog IO |
| `eletechsup_nt18b07` | 7-ch NTC temperature sensor |
| `eastron_sdm120m` | Single-phase energy meter |
| `aermec_hmi080` | Heat-pump HMI controller |
| `eneren_rer_020i` | HVAC ERV unit (Eneren RER020I) |
| `waveshare_rtu_relay` | Waveshare RS-485 relay |
| `xy_mod01_sht20` | SHT20 temperature/humidity sensor |
| `gl_th02_pe` | Gauselink temperature/humidity sensor |

---

## Requirements

- Home Assistant 2024.x or newer
- The built-in `modbus` integration must be available (it ships with HA Core)
- A working Modbus TCP gateway (RTU-over-TCP, TCP, or UDP) accessible from the HA host

---

## Installation

1. Copy the `custom_components/drp_modbus_boards_v2` directory into your HA `config/custom_components/` folder.
2. Restart Home Assistant.
3. Open **Settings → Devices & Services → Add Integration**, search for **Modbus Boards (DRP)**, and add it. This step creates a UI placeholder entry; actual hub configuration is done in YAML.

---

## Configuration

All hub and device configuration lives in `configuration.yaml`. The integration domain key is `drp_modbus_boards_v2`.

### Minimal example

```yaml
drp_modbus_boards_v2:
  - name: my_modbus_hub
    type: tcp           # tcp | udp | rtuovertcp
    host: 192.168.1.100
    port: 502
    scan_interval: 30   # seconds, default 30

    devices:
      - board: eletechsup_n4rod08
        slave: 1
        name: Relay Board

        switches:
          - name: Relay 1
            device_function: channel_00
          - name: Relay 2
            device_function: channel_01
```

### Full device block options

```yaml
devices:
  - board: <board_identifier>       # required — see table above
    slave: <1–247>                  # required — Modbus slave address
    name: <string>                  # required — used as HA device name
    entity_constraint: <entity_id>  # optional — only poll when this entity is ON

    sensors:
      - name: <string>
        device_function: <function> # defined by the board model
        unique_id: <string>         # optional, auto-generated if omitted
        used_entity: true           # optional, default true
        offset: 0                   # optional numeric offset added after scaling
        device_class: <class>
        state_class: <class>
        unit_of_measurement: <unit>

    binary_sensors:
      - name: <string>
        device_function: <function>
        device_class: <class>

    switches:
      - name: <string>
        device_function: <function>
        reverse: false              # optional, inverts ON/OFF logic

    numbers:
      - name: <string>
        device_function: <function>
        mode: slider                # slider | box | auto
        unit_of_measurement: <unit>
        device_class: <class>
```

### N4DBA06 example (analog IO board)

```yaml
drp_modbus_boards_v2:
  - name: analog_hub
    type: rtuovertcp
    host: 192.168.1.50
    port: 8899
    scan_interval: 10

    devices:
      - board: eletechsup_n4dba06
        slave: 1
        name: Analog IO Board

        sensors:
          - name: Input Voltage Vi2
            device_function: voltage_in2
            device_class: voltage
            unit_of_measurement: V

          - name: Input Vi2 Percent
            device_function: voltage_in2_percentage
            unit_of_measurement: "%"

        numbers:
          - name: Output Voltage Vo2
            device_function: voltage_out2
            device_class: voltage
            unit_of_measurement: V

        switches:
          - name: Digital Output
            device_function: channel_00
```

### Reload service

After editing `configuration.yaml` you can reload the integration without restarting HA:

```yaml
# Developer Tools → Services
service: drp_modbus_boards_v2.reload
```

---

## Available `device_function` values by board

### eletechsup_n4dba06

| Platform | `device_function` | Description |
|---|---|---|
| sensor | `voltage_in2` | Vi2 voltage input, 0–10 V |
| sensor | `voltage_in2_percentage` | Vi2 as 0–100 % |
| number | `voltage_out2` | Vo2 voltage output setpoint, 0.1–10 V |
| number | `voltage_out2_percentage` | Vo2 output as percentage |
| switch | `channel_00` | Digital output DoP/DoN |

### eletechsup_n4rod08

Provides `channel_00` through `channel_07` on the `switch` platform.

### Generic multi-channel boards (relay/IO)

Relay and IO boards generally expose channels as `channel_00` … `channel_N` on `switch` and/or `sensor` platforms. Refer to each board's model file under `domain/models/` for the full list.

---

## entity_constraint

When set, the integration skips polling the device unless the referenced HA entity is in state `on`. This is useful for saving bus bandwidth on devices that should only be queried while a system is running.

```yaml
- board: eletechsup_n4dba06
  slave: 2
  name: HVAC Analog Board
  entity_constraint: binary_sensor.hvac_power_state
```

---

## Developer Guide

### Architecture overview

The integration follows a layered design:

```
configuration.yaml
       │
  async_setup()          ← __init__.py, parses YAML, manages ConfigEntries
       │
  async_setup_entry()    ← creates ModbusCoordinator, starts Modbus hub
       │
  ModbusCoordinator      ← controller/coordinator.py, DataUpdateCoordinator
       │  polls every scan_interval
       ▼
  async_modbus_read_area()  ← helpers/modbus.py, raw Modbus reads per RegisterArea
       │
  hass.data[DOMAIN][device_areas_data][key]   ← shared in-memory register cache
       │
  BaseEntityClass        ← helpers/base_entity_class.py, consumed by each platform
```

Each HA platform (sensor, switch, binary_sensor, number) has its own file at the top level (`sensor.py`, `switch.py`, etc.) and extends `BaseEntityClass`.

### Adding a new board

1. **Create an enum entry** in `domain/enums.py`:
   ```python
   class Board(StrEnum):
       MY_NEW_BOARD = "my_new_board"
   ```

2. **Create a model file** `domain/models/my_new_board.py`. Use the `@register_board` decorator:

   ```python
   from ..boards import BoardDefinition, Metadata, Register, RegisterArea, RegisterFunction, RegisterFunctionRead
   from ..enums import Board, RegisterAreaName, SensorFunction
   from ...helpers.boards import register_board
   from homeassistant.components.modbus.const import CALL_TYPE_REGISTER_HOLDING, DataType
   from homeassistant.const import Platform

   @register_board(Board.MY_NEW_BOARD)
   def _my_new_board_regs():
       return BoardDefinition(
           metadata=Metadata(name="My Board", manufacturer="acme", model="xyz"),
           areas={
               RegisterAreaName.AREA_A: RegisterArea(
                   address=0x0000,
                   count=4,
                   mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                   data_type=DataType.UINT16,
               ),
           },
           registers={
               Platform.SENSOR: Register(
                   functions={
                       SensorFunction.TEMPERATURE: RegisterFunction(
                           area=RegisterAreaName.AREA_A,
                           address=0x0000,
                           function_read=RegisterFunctionRead(scale=0.1, precision=1),
                           min=-40, max=85,
                           state_class="measurement",
                           device_class="temperature",
                           unit_of_measurement="°C",
                       ),
                   }
               ),
           },
       )
   ```

3. **Import the module** in `__init__.py`:
   ```python
   from .domain.models import my_new_board  # noqa: F401
   ```

4. **Register the board string** in the `MODBUS_SCHEMA` validator inside `domain/schema.py`:
   ```python
   vol.Required(CONF_BOARD): vol.In([
       ...
       Board.MY_NEW_BOARD,
   ]),
   ```

5. **Add enum functions** (optional) to `domain/enums.py` if your board needs function names not already present in `SensorFunction`, `SwitchFunction`, or `NumberFunction`.

### Key domain concepts

#### `RegisterArea`

Describes a **contiguous block of Modbus registers** to read in a single request. Fields:

| Field | Purpose |
|---|---|
| `address` | Starting register address (absolute, as per board datasheet) |
| `count` | Number of registers to read |
| `mdb_read_function` | Modbus function code for reads (`CALL_TYPE_REGISTER_HOLDING`, `CALL_TYPE_REGISTER_INPUT`) |
| `mdb_write_function` | Modbus function code for writes (`CALL_TYPE_WRITE_REGISTER`), `None` if read-only |
| `data_type` | `DataType.UINT16`, `DataType.FLOAT32`, etc. |
| `registry_area_shift` | Offset subtracted from a register's absolute address to compute its index within the raw response array. Set this when the register block does not start at address 0 (e.g. output registers starting at `0x0080` need `registry_area_shift = -0x80`). |
| `state_on / state_off` | Raw register values that represent ON/OFF for switches and binary sensors |
| `command_on / command_off` | Raw values written to the register to turn ON/OFF |

#### `RegisterFunction`

Maps a **single named HA entity** to a specific register within an area:

| Field | Purpose |
|---|---|
| `area` | Which `RegisterAreaName` this entity reads from |
| `address` | Absolute register address (the area's `registry_area_shift` is applied automatically) |
| `function_read` | `RegisterFunctionRead(scale, precision, state_on, state_off)` |
| `function_write` | `RegisterFunctionWrite(scale, step, number_mode, command_on, command_off)` |
| `min / max` | Valid value range; values outside this range are discarded |
| `device_class`, `state_class`, `unit_of_measurement` | Standard HA entity metadata |

#### Scale convention

The register value read from hardware is always an integer. `scale` converts it to a physical unit:

```
physical_value = raw_integer × scale
```

For example, a register holding `330` with `scale=0.01` yields `3.30 V`. For **write** operations the inverse applies: the HA numeric value is multiplied by the write `scale` before being sent to the bus.

#### Board registry

Boards are registered lazily via the `@register_board` decorator. The global `_REGISTRY` dictionary (in `helpers/boards.py`) maps a board key string to a factory function. Boards are only instantiated on first use. You can enumerate all registered boards with `get_boards()`.

### Data flow during a poll cycle

1. `ModbusCoordinator._async_update_data()` iterates over all configured devices and their `RegisterArea`s.
2. For each area, `async_modbus_read_area()` issues a single Modbus read request and stores the raw response in `hass.data[DOMAIN]["device_areas_data"][key]`, where `key` is derived from `board + slave + area_name`.
3. Each `BaseEntityClass` entity calls `get_stored_board_data_area()` on coordinator update, extracts its register value via `get_value_from_modbus_response()`, and transforms it with `transform_from_modbus_raw_value()` (applies scale, precision, min/max, and type coercion).

### Write path (switch / number)

Write operations bypass the coordinator poll and go directly through `ModbusHub`. The entity:
1. Applies the write `scale` to convert the HA value to a raw integer.
2. Calls `async_pb_call()` on the hub with `CALL_TYPE_WRITE_REGISTER` and the computed raw value.
3. Requests a coordinator refresh so the new state is reflected immediately.

### Adding a new HA platform function

If a board needs a function key that does not yet exist (e.g. a current output), add it to the appropriate `StrEnum` in `domain/enums.py` (e.g. `SensorFunction`, `NumberFunction`). The string value becomes the `device_function` value users put in their YAML.

---

## License

See [LICENSE](LICENSE).