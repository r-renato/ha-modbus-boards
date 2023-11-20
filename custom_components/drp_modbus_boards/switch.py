"""Support for Modbus switches."""
from __future__ import annotations

from typing import Any
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME, CONF_SWITCHES, CONF_FRIENDLY_NAME, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import get_hub
from .const import (
    CONF_BOARD,
    BOARD_SWITCHES,
    CONF_REVERSE,
    BOARDS_AND_REGISTERS,
    Platform,
)
from .base_platform import BaseSwitch
from .modbus import ModbusHub

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Read configuration and create Modbus switches."""
    switches = []

    if discovery_info is None:
        return

    for switch in discovery_info[CONF_SWITCHES]:
        board_registries = BOARDS_AND_REGISTERS[ switch.get(CONF_BOARD) ][ Platform.SWITCH ]
        
        for int_switch in switch.get(CONF_SWITCHES, None):
            registry = int_switch.get(CONF_NAME)
            if registry in board_registries:
                _LOGGER.debug( 'async_setup_platform add switch for board %s and registry %s', switch.get(CONF_BOARD), registry )
                hub: ModbusHub = get_hub(hass, discovery_info[CONF_NAME])
                switches.append(ModbusSwitch(hub, switch, int_switch))
            else:
                _LOGGER.warning( 'async_setup_platform switch for board %s, registry %s not exist.', switch.get(CONF_BOARD), registry )                
    async_add_entities(switches)

class ModbusSwitch(BaseSwitch, SwitchEntity):
    """Base class representing a Modbus switch."""

    def __init__(
        self,
        hub: ModbusHub,
        entry: dict[str, Any],
        internal_switch: dict[str, Any],
    ) -> None:
        """Initialize the modbus register sensor."""
        super().__init__(hub, entry)

        self._attr_board = entry.get(CONF_BOARD)
        self._attr_switch = internal_switch.get(CONF_NAME)
        self._register = BOARDS_AND_REGISTERS[self._attr_board ][ Platform.SWITCH ][ self._attr_switch ]
        
        self._address = self._register[ 4 ]
        self._write_type = self._register[ 5 ]
        self.command_on = self._register[ 6 ] if not internal_switch.get(CONF_REVERSE) else self._register[ 7 ]
        self._command_off = self._register[ 7 ] if not internal_switch.get(CONF_REVERSE) else self._register[ 6 ]

        self._verify_active = True
        self._verify_delay = 5
        self._verify_address = self._register[ 0 ]
        self._verify_type = self._register[ 1 ]
        self._state_on = self._register[ 2 ] if not internal_switch.get(CONF_REVERSE) else self._register[ 3 ]
        self._state_off = self._register[ 3 ] if not internal_switch.get(CONF_REVERSE) else self._register[ 2 ]

        self._attr_name =  internal_switch.get(CONF_FRIENDLY_NAME, self._attr_name + ' ' + self._register[ 8 ]) 
        self._attr_unique_id = internal_switch.get(CONF_UNIQUE_ID, self._attr_unique_id + '_' + self._register[ 8 ] if self._attr_unique_id else self._attr_name)

        self._attr_manufacturer = self._register[ 9 ]
        self._attr_model = self._register[ 10 ]

        _LOGGER.debug( '### switch initialized slave:%d, address:%d, write_type:%s, operation:%s, on:%s, off:%s, son:%s, soff:%s %s', 
             self._slave, self._address, str(self._write_type), self._input_type, 
             str(self.command_on), str(self._command_off), str(self._state_on), str(self._state_off), str(internal_switch.get(CONF_REVERSE)) )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set switch on."""
        await self.async_turn(self.command_on)