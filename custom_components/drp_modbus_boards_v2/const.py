"""Costanti per DRP Modbus Boards."""
from __future__ import annotations

import logging

from functools import lru_cache
from typing import NamedTuple

from homeassistant.const import (
    Platform,
)

from importlib.resources import files  # Python 3.9+

import json

_LOGGER = logging.getLogger(__name__)


# --- Metadati integrazione ----------------------------------------------------
class IntegrationMeta(NamedTuple):
    """Metadati dell'integrazione."""
    domain: str
    name: str
    version: str
    manufacturer: str
    issue_url: str

@lru_cache(maxsize=1)
def load_integration_meta(pkg: str = __package__ or "const") -> IntegrationMeta:
    """
    Legge manifest.json come risorsa del pacchetto (portabile anche con zipimport).
    Ritorna fallback sicuri se mancante/corrotto.
    """
    default = IntegrationMeta("N/A", "Unknown Integration", "N/A", "N/A", "N/A")
    try:
        text = (files(pkg) / "manifest.json").read_text(encoding="utf-8")
        data = json.loads(text)
        return IntegrationMeta(
            data.get("domain", default.domain),
            data.get("name", default.name),
            data.get("version", default.version),
            data.get("manufacturer", default.manufacturer),
            data.get("issue_tracker") or data.get("issue_url") or default.issue_url,
        )
    except Exception as e:
        _LOGGER.error("Manifest read error for %s: %s", pkg, e)
        return default

def make_startup_banner(meta: IntegrationMeta) -> str:
    """Crea il banner di avvio dell'integrazione."""
    return (
        "-------------------------------------------------------------------\n"
        f"{meta.name}\n"
        f"Version: {meta.version}\n"
        "This is a custom integration!\n"
        "If you have any issues with this you need to open an issue here:\n"
        f"{meta.issue_url}\n"
        "-------------------------------------------------------------------"
    )

_META = load_integration_meta()   # __package__ punta a custom_components.<domain>
DOMAIN, INTEGRATION_NAME, INTEGRATION_VERSION, INTEGRATION_MANUFACTURER, INTEGRATION_ISSUE_URL = _META
STARTUP_MESSAGE = make_startup_banner(_META)

PLATFORMS = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
]

# integration names
DEFAULT_HUB = "drp_modbus_boards_hub"

COORDINATORS = "coordinators"
DEVICE_AREAS_DATA = "device_areas_data"

# --- Metadati Schema ----------------------------------------------------
DEFAULT_SCAN_INTERVAL = 30  # seconds

CONF_DEVICES = "devices"
CONF_DEVICE_FUNCTION = "device_function"

CONF_BOARD = "board"
CONF_ENTITY_CONSTRAINT = "entity_constraint"
CONF_USED_ENTITY = "used_entity"

CONF_LAZY_ERROR = "lazy_error_count"
CONF_NUMBERS = "numbers"
CONF_REVERSE = "reverse"

MODE_SLIDER = "slider"
MODE_BOX = "box"
MODE_AUTO = "auto"

CONF_CLOSE_COMM_ON_ERROR = "close_comm_on_error"
CONF_RETRIES = "retries"
CONF_RETRY_ON_EMPTY = "retry_on_empty"
CONF_MSG_WAIT = "message_wait_milliseconds"















