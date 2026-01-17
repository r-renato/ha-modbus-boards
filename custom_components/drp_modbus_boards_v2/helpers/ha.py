"""..."""
from __future__ import annotations
from typing import Protocol

import logging

from homeassistant.core import HomeAssistant, State
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

class ModbusConstLike(Protocol):
    """Protocol for Modbus const-like objects."""
    PLATFORMS: tuple[tuple[Platform, str], ...]

def ensure_number_in_platforms(modbus_const: ModbusConstLike, conf_numbers: str) -> None:
    """Ensure that the NUMBER platform is registered in modbus_const."""
    current = modbus_const.PLATFORMS
    if any(p is Platform.NUMBER for p, _ in current):
        return
    modbus_const.PLATFORMS = (*current, (Platform.NUMBER, conf_numbers))

def resolve_sensor_device_class(value: str | None) -> SensorDeviceClass | None:
    """Converte una stringa in SensorDeviceClass, se possibile."""
    if not value:
        return None

    # normalizza in minuscolo (le enum usano 'temperature', 'energy', ecc.)
    normalized = value.lower()

    try:
        return SensorDeviceClass(normalized)
    except ValueError:
        # valore non valido: log e ignora
        _LOGGER.warning(
            "Device class '%s' non valida per sensore, verrà ignorata",
            value,
        )
        return None


def resolve_sensor_state_class(value: str | None) -> SensorStateClass | None:
    """Converte una stringa in SensorStateClass, se possibile."""
    if not value:
        return None

    normalized = value.lower()

    try:
        return SensorStateClass(normalized)
    except ValueError:
        _LOGGER.warning(
            "State class '%s' non valida per sensore, verrà ignorata",
            value,
        )
        return None

def entity_state(hass: HomeAssistant, entity_id: str | None) -> State | None:
    """Restituisce lo stato di un'entità HA, o None se non disponibile."""
    if not entity_id:
        return None
    return hass.states.get(entity_id)


