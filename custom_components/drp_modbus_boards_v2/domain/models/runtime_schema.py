#  models for Modbus-based entities, devices, and hubs.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from homeassistant.components.sensor.const import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.components.number import NumberDeviceClass

from ..enums import Board
from ...const import (
    MODE_SLIDER,
)

# ---------------------------------------------------------------------------
# Base entity  models
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BaseEntity:
    """Common  fields for all entities (sensor, binary_sensor, switch, number)."""

    name: str
    device_function: str  # CONF_DEVICE_FUNCTION
    unique_id: Optional[str] = None
    used_entity: Optional[bool] = True  # CONF_SWITCH_CONSTRAINT at entity level


@dataclass(frozen=True)
class SensorConfig(BaseEntity):
    """ representation of a Modbus-based sensor."""

    offset_value: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    nan_value: Optional[float] = None
    zero_suppress: Optional[float] = None

    device_class: Optional[SensorDeviceClass] = None
    state_class: Optional[SensorStateClass] = None
    unit_of_measurement: Optional[str] = None


@dataclass(frozen=True)
class BinarySensorConfig(BaseEntity):
    """ representation of a Modbus-based binary sensor."""

    device_class: Optional[BinarySensorDeviceClass] = None


@dataclass(frozen=True)
class SwitchConfig(BaseEntity):
    """ representation of a Modbus-based switch."""

    reverse: bool = False
    device_class: Optional[SwitchDeviceClass] = None


@dataclass(frozen=True)
class NumberConfig(BaseEntity):
    """ representation of a Modbus-based number (setpoint, etc.)."""

    icon: Optional[str] = None
    unit_of_measurement: Optional[str] = None
    mode: str = MODE_SLIDER  # one of MODE_AUTO | MODE_BOX | MODE_SLIDER
    device_class: Optional[NumberDeviceClass] = None

# ---------------------------------------------------------------------------
# Device and hub  models (non-flattened structure)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DeviceConfig:
    """ representation of a Modbus device (board instance)."""

    board: Board
    slave: int
    name: str
    entity_constraint: Optional[str] = None  # CONF_ENTITY_CONSTRAINT at device level

    sensors: List[SensorConfig] = field(default_factory=list)
    binary_sensors: List[BinarySensorConfig] = field(default_factory=list)
    switches: List[SwitchConfig] = field(default_factory=list)
    numbers: List[NumberConfig] = field(default_factory=list)

@dataclass(frozen=True)
class RuntimeEntryConfig:
    """ representation of a Modbus hub (TCP/UDP/RTU-over-TCP)."""

    name: str
    host: str
    port: int
    type: str  # one of TCP, UDP, RTUOVERTCP
    scan_interval: int

    boards: List[Board] = field(default_factory=list)
    devices: List[DeviceConfig] = field(default_factory=list)
