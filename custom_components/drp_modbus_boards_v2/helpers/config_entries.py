"""Builder utilities to create non-flattened runtime models from CONFIG_SCHEMA.

This module maps the validated Home Assistant configuration (after MODBUS_SCHEMA /
ETHERNET_SCHEMA / CONFIG_SCHEMA validation) into the immutable runtime models
defined in the sibling runtime module (HubRuntime, DeviceConfig, ...).
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Optional, Union, Callable

from homeassistant.core import HomeAssistant, Event, CALLBACK_TYPE, EventStateChangedData
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.components.modbus.const import (
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_NAN_VALUE,
    CONF_ZERO_SUPPRESS,
)
from homeassistant.components.sensor.const import CONF_STATE_CLASS
from homeassistant.const import (
    CONF_SLAVE,
    CONF_BINARY_SENSORS,
    CONF_DEVICE_CLASS,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_OFFSET,
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_SWITCHES,
    CONF_TYPE,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ICON,
    CONF_MODE,
    CONF_TIMEOUT,
    CONF_DELAY,
)

from ..helpers.utils import slugify
from ..helpers.logger import log_info

from ..domain.enums import Board
from ..const import (
    CONF_BOARD,
    CONF_DEVICE_FUNCTION,
    CONF_DEVICES,
    CONF_ENTITY_CONSTRAINT,
    CONF_NUMBERS,
    CONF_REVERSE,
    CONF_USED_ENTITY,
    DEFAULT_HUB,
    MODE_SLIDER,
)

from ..domain.models.runtime_schema import (  # adjust the module name to match your project layout
    SensorConfig,
    BinarySensorConfig,
    SwitchConfig,
    NumberConfig,
    DeviceConfig,
    RuntimeEntryConfig,
)

_LOGGER = logging.getLogger(__name__)

def subscribe_entity_state_changes(
    hass: HomeAssistant,
    callback: Callable[[Event[EventStateChangedData]], Any],   # 👈 firma richiesta
    entity_ids: Union[str, Iterable[str]],
    *,
    on_remove: Optional[Callable[[CALLBACK_TYPE], None]] = None,
) -> Optional[CALLBACK_TYPE]:
    """
    Sottoscrive gli eventi `state_changed` per uno o più `entity_id` e restituisce
    la **funzione di unsubscribe**.

    Questo helper è un thin-wrapper su `async_track_state_change_event` che:
    - accetta una stringa singola o un iterabile di `entity_id`;
    - normalizza e **deduplica** gli ID vuoti o ripetuti;
    - opzionalmente registra l’unsubscribe nel ciclo di vita passato in `on_remove`
      (es. `entry.async_on_unload`, `entity.async_on_remove`).

    Parametri
    ---------
    hass : HomeAssistant
        Istanza di Home Assistant.
    callback : Callable[[Event[EventStateChangedData]], Any]
        Handler invocato su ogni evento `state_changed` degli entity monitorati.
        Può essere sincrono (consigliato decorare con `@callback`) o `async def`.
        Firma tip-safe: `def handler(event: Event[EventStateChangedData]) -> None`.
    entity_ids : str | Iterable[str]
        Uno o più `entity_id` (es. `"sensor.t_living"` o `["sensor.t_living", "sensor.h_living"]`).
    on_remove : Callable[[CALLBACK_TYPE], None], opzionale
        Funzione alla quale passare la `unsubscribe` per legarla al ciclo di vita
        (es. `entry.async_on_unload`, `self.async_on_remove`).
    log : bool, opzionale
        Se `True` logga l’attivazione dell’ascolto.

    Ritorno
    -------
    Optional[CALLBACK_TYPE]
        La funzione di **unsubscribe** (richiamala per rimuovere il listener),
        oppure `None` se `entity_ids` non contiene elementi validi.

    Esempi
    -------
    >>> # In config entry setup:
    >>> unsub = subscribe_entity_state_changes(
    ...     hass,
    ...     callback=my_handler,                              # def my_handler(e: Event[EventStateChangedData]) -> None
    ...     entity_ids=["sensor.t_soggiorno", "sensor.h_soggiorno"],
    ...     on_remove=entry.async_on_unload,                  # si pulisce da solo allo unload dell'entry
    ... )
    ...
    >>> # Dentro una Entity:
    >>> self._unsub = subscribe_entity_state_changes(
    ...     self.hass, my_handler, "sensor.t_camera", on_remove=self.async_on_remove
    ... )

    Note
    ----
    - Preferisci handler **sincroni** con `@callback` per ridurre overhead.
    - La firma della callback è tipizzata come `Event[EventStateChangedData]` per
      essere compatibile con `async_track_state_change_event` su HA 2025.4.x+.
    """
    # Normalizza gli entity_id
    ids: List[str]
    if isinstance(entity_ids, str):
        ids = [entity_ids]
    else:
        ids = [e for e in entity_ids if isinstance(e, str) and e.strip()]

    if not ids:
        _LOGGER.error("setup_entity_change: nessun entity_id valido.")
        return None

    unsubscribe: CALLBACK_TYPE = async_track_state_change_event(hass, ids, callback)
    log_info(_LOGGER, "Ascolto attivo per %s", ", ".join(ids))

    if on_remove is not None:
        try:
            on_remove(unsubscribe)
        except Exception:
            _LOGGER.exception("setup_entity_change: on_remove ha generato un'eccezione.")

    return unsubscribe

# ---------------------------------------------------------------------------
# Internal helpers: per-entity-type builders
# ---------------------------------------------------------------------------


def _build_sensors(device_cfg: Dict[str, Any]) -> List[SensorConfig]:
    """Build the list of SensorConfig for a single device config."""

    sensors: List[SensorConfig] = []

    for s_cfg in device_cfg.get(CONF_SENSORS, []):
        sensors.append(
            SensorConfig(
                name=s_cfg[CONF_NAME],
                device_function=s_cfg[CONF_DEVICE_FUNCTION],
                unique_id=s_cfg.get(CONF_UNIQUE_ID),
                used_entity=s_cfg.get(CONF_USED_ENTITY),
                offset_value=s_cfg.get(CONF_OFFSET),
                min_value=s_cfg.get(CONF_MIN_VALUE),
                max_value=s_cfg.get(CONF_MAX_VALUE),
                nan_value=s_cfg.get(CONF_NAN_VALUE),
                zero_suppress=s_cfg.get(CONF_ZERO_SUPPRESS),
                device_class=s_cfg.get(CONF_DEVICE_CLASS),
                state_class=s_cfg.get(CONF_STATE_CLASS),
                unit_of_measurement=s_cfg.get(CONF_UNIT_OF_MEASUREMENT),
            )
        )

    return sensors


def _build_binary_sensors(device_cfg: Dict[str, Any]) -> List[BinarySensorConfig]:
    """Build the list of BinarySensorConfig for a single device config."""

    binary_sensors: List[BinarySensorConfig] = []

    for b_cfg in device_cfg.get(CONF_BINARY_SENSORS, []):
        binary_sensors.append(
            BinarySensorConfig(
                name=b_cfg[CONF_NAME],
                device_function=b_cfg[CONF_DEVICE_FUNCTION],
                unique_id=b_cfg.get(CONF_UNIQUE_ID),
                used_entity=b_cfg.get(CONF_USED_ENTITY),
                device_class=b_cfg.get(CONF_DEVICE_CLASS),
            )
        )

    return binary_sensors

def _build_switches(device_cfg: Dict[str, Any]) -> List[SwitchConfig]:
    """Build the list of SwitchConfig for a single device config."""

    switches: List[SwitchConfig] = []

    for sw_cfg in device_cfg.get(CONF_SWITCHES, []):
        switches.append(
            SwitchConfig(
                name=sw_cfg[CONF_NAME],
                device_function=sw_cfg[CONF_DEVICE_FUNCTION],
                unique_id=sw_cfg.get(CONF_UNIQUE_ID),
                used_entity=sw_cfg.get(CONF_USED_ENTITY),
                reverse=sw_cfg.get(CONF_REVERSE, False),
                device_class=sw_cfg.get(CONF_DEVICE_CLASS),
            )
        )

    return switches


def _build_numbers(device_cfg: Dict[str, Any]) -> List[NumberConfig]:
    """Build the list of NumberConfig for a single device config."""

    numbers: List[NumberConfig] = []

    for n_cfg in device_cfg.get(CONF_NUMBERS, []):
        numbers.append(
            NumberConfig(
                name=n_cfg[CONF_NAME],
                device_function=n_cfg[CONF_DEVICE_FUNCTION],
                unique_id=n_cfg.get(CONF_UNIQUE_ID),
                used_entity=n_cfg.get(CONF_USED_ENTITY),
                icon=n_cfg.get(CONF_ICON),
                unit_of_measurement=n_cfg.get(CONF_UNIT_OF_MEASUREMENT),
                mode=n_cfg.get(CONF_MODE, MODE_SLIDER),
                device_class=n_cfg.get(CONF_DEVICE_CLASS),
            )
        )

    return numbers

# ---------------------------------------------------------------------------
# Device and hub builders
# ---------------------------------------------------------------------------

def _build_devices(hub_cfg: Dict[str, Any]) -> List[DeviceConfig]:
    """Build the list of DeviceConfig for a single hub config."""

    devices: List[DeviceConfig] = []

    for dev_cfg in hub_cfg.get(CONF_DEVICES, []):
        sensors = _build_sensors(dev_cfg)
        binary_sensors = _build_binary_sensors(dev_cfg)
        switches = _build_switches(dev_cfg)
        numbers = _build_numbers(dev_cfg)

        devices.append(
            DeviceConfig(
                board=dev_cfg[CONF_BOARD],
                slave=dev_cfg[CONF_SLAVE],
                name=dev_cfg[CONF_NAME],
                entity_constraint=dev_cfg.get(CONF_ENTITY_CONSTRAINT),
                sensors=sensors,
                binary_sensors=binary_sensors,
                switches=switches,
                numbers=numbers,
            )
        )

    return devices


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_runtime_schema(config: Dict[str, Any]) -> RuntimeEntryConfig:
    """Build a non-flattened list of HubRuntime from validated CONFIG_SCHEMA.

    Expected input *config* format (after CONFIG_SCHEMA validation):

        config[DOMAIN] -> list of hub dictionaries (ETHERNET_SCHEMA instances), e.g.::

            [
                {
                    "name": "Hub1",
                    "host": "192.168.1.10",
                    "port": 502,
                    "type": "tcp",
                    "devices": [...],
                },
                ...
            ]

    This function preserves the hierarchy:

        HubRuntime -> DeviceConfig -> [SensorConfig | BinarySensorConfig | SwitchConfig | NumberConfig]

    without flattening entities across hubs/devices.
    """

    boards: List[Board] = []
    devices = _build_devices(config)

    for device_config in devices:
        boards.append(device_config.board)

    return RuntimeEntryConfig(
                name=config[CONF_NAME],
                host=config[CONF_HOST],
                port=config[CONF_PORT],
                type=config[CONF_TYPE],
                scan_interval=config[CONF_SCAN_INTERVAL],
                boards=boards,
                devices=devices,
            )

def build_modbus_ha_config(modbus_board_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Costruisce un dict 'slim' per Modbus core partendo da un hub v2.

    Prende SOLO i campi necessari al trasporto Modbus:
    - name
    - type
    - host / port (per TCP/UDP/RTU-over-TCP)
    - port + parametri seriali (per SERIAL)
    - timeout
    - delay

    Tutta la parte custom (devices, switches, ecc.) viene ignorata qui.

    ATTENZIONE!!! Non modificare
    """

    slim: Dict[str, Any] = {
        CONF_NAME: modbus_board_config.get(CONF_NAME, DEFAULT_HUB),
        CONF_TYPE: modbus_board_config[CONF_TYPE],
        CONF_HOST: modbus_board_config[CONF_HOST],
        CONF_PORT: modbus_board_config[CONF_PORT],

        CONF_TIMEOUT: modbus_board_config.get(CONF_TIMEOUT),
        CONF_DELAY: modbus_board_config.get(CONF_DELAY),

        CONF_SENSORS: [{
            CONF_NAME: "Placeholder Sensor",
        }],
    }

    return [slim]
