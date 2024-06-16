"""Support for Modbus switches."""
from __future__ import annotations

import time
from random import randint
import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_FRIENDLY_NAME,
    CONF_SWITCHES,
    CONF_UNIQUE_ID,
    CONF_SLAVE,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_call_later, async_track_time_interval
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.restore_state import RestoreEntity

from . import get_hub
from .const import CONF_DEVICE_ADDRESS, DataType
from .base_platform import BoardsBaseSwitch, BoardsBaseSlaveSwitch, DataProcessing
from .modbus import ModbusHub

from .boards_const import (
    CONF_BOARD,
    CONF_REVERSE,
    BOARDS,
    BoardBlock,
    BoardMetadataRegIdx,
    SwitchRegIdx,
    # RBD_BLOCK_NAME,
    # RBD_BLOCK_NDX,
    # BLK_STATE_CLOSE,
    # BLK_STATE_OPEN,
    # WBD_GUIDE,
    METADATA,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1    


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Read configuration and create Modbus switches."""
    # switches = []

    if discovery_info is None:
        return

    # for entry in discovery_info[CONF_SWITCHES]:
    #     hub: ModbusHub = get_hub(hass, discovery_info[CONF_NAME])
    #     switches.append(ModbusSwitch(hass, hub, entry))
    # async_add_entities(switches)

    switches: list[ModbusSwitch | SlaveModbusSwitch] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for conf_switches in discovery_info[CONF_SWITCHES]:
        board_registries = BOARDS[ conf_switches.get(CONF_BOARD) ][ Platform.SWITCH ]
        slave_count = 0
        slaves: list[SlaveModbusSwitch] = []
        for int_sensor in conf_switches.get(CONF_SWITCHES, None):
            device_name = int_sensor.get(CONF_NAME)
            if device_name in board_registries:
                _LOGGER.debug( 'async_setup_platform for board %s, add switch %s', conf_switches.get(CONF_BOARD), device_name )
                
                if slave_count > 0:
                    slaves.append(await new_switch.async_setup_slaves(hass, slave_count, conf_switches, int_sensor))
                else:
                    new_switch = ModbusSwitch(hass, hub, conf_switches, slave_count, int_sensor)
                slave_count += 1
            else:
                _LOGGER.warning( 'async_setup_platform for board %s, switch %s not exist.', conf_switches.get(CONF_BOARD), device_name )
        switches.extend(slaves)
        switches.append(new_switch)
    async_add_entities(switches)


class ModbusSwitch(BoardsBaseSwitch, SwitchEntity):
    """Base class representing a Modbus switch."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        entry: dict[str, Any],
        slave_count: int,
        internal_switch: dict[str, Any],
    ) -> None:
        """Initialize the modbus register sensor."""
        super().__init__(hass, hub, entry, Platform.SWITCH, internal_switch.get(CONF_NAME))

        self._slave_count = slave_count
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._attr_name =  internal_switch.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_switch.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + self._attr_sensor_name + ' id ' + str(self._slave)
        ).replace(" ", "_")

        self._attr_manufacturer = self._attr_metadata[ 0 ]
        self._attr_model = self._attr_metadata[ 1 ]

        if internal_switch.get(CONF_REVERSE):
            old = self.command_on
            self.command_on = self._command_off
            self._command_off = old
            old = self._state_on
            self._state_on = self._state_off
            self._state_off = old

        _LOGGER.info( "Setup for '%s' slave:'%s'", 
            self._attr_board, self._slave)

    async def async_setup_slaves(
        self, hass: HomeAssistant, slave_count: int, entry: dict[str, Any], internal_switches: dict[str, Any]
    ) -> list[SlaveModbusSwitch]:
        """Add slaves as needed (1 read for multiple sensors)."""

        # Add a dataCoordinator for each sensor that have slaves
        # this ensures that idx = bit position of value in result
        # polling is done with the base class
        name = self._attr_name if self._attr_name else "modbus_switch"
        if self._coordinator is None:
            self._coordinator = DataUpdateCoordinator(
                hass,
                _LOGGER,
                name=name,
            )

        return SlaveModbusSwitch(hass, self._hub, self._coordinator, entry, slave_count, internal_switches)

    async def async_update(self, now: datetime | None = None) -> None:
        start_time = time.perf_counter()
        if not self._platform_ready:
            self._cancel_call = async_call_later(
                self.hass, timedelta(seconds=randint(30, 60)), self.async_update
            )
            _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error not self._platform_ready.", 
                round(time.perf_counter()-start_time, 2), self._attr_board, self._slave)
            return
        
        if self._update_lock_flag:
            _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error self._update_lock_flag.", 
                round(time.perf_counter()-start_time, 2), self._attr_board, self._slave)
            return
        
        if self._state_constraint != 'on':
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error self._state_constraint != 'on'.", 
                round(time.perf_counter()-start_time, 2), self._attr_board, self._slave)
            return  
        
        async with self._update_lock:
            self._update_lock_flag = True
            self._cancel_call = None
            operation = await self.async_board_read_data(Platform.SWITCH)
            sensor_data = self._attr_board_blocks[self._attr_sensor_registers[SwitchRegIdx.BLOCK_NAME]]
            
            if not operation or not sensor_data or not hasattr(sensor_data, "registers"):
                if self._lazy_errors:
                    self._lazy_errors -= 1
                    self._cancel_call = async_call_later(
                        self.hass, timedelta(seconds=1), self.async_update
                    )
                    self._update_lock_flag = False
                    _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error not operation or not sensor_data or not hasattr.", 
                        round(time.perf_counter()-start_time, 2), self._attr_board, self._slave)                    
                    return
                self._lazy_errors = self._lazy_error_count

                self._attr_available = False
                self._attr_native_value = None
                if self._coordinator:
                    self._coordinator.async_set_updated_data(None)
                self.async_write_ha_state()
                self._update_lock_flag = False
                _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error reading data.", 
                    round(time.perf_counter()-start_time, 2), self._attr_board, self._slave)
                return

            result = self._decode_state(sensor_data)

            if result is None:
                self._attr_available = False
            elif result:
                self._attr_available = True
                self._attr_is_on = True
            else:
                self._attr_available = True
                self._attr_is_on = False

            if self._coordinator:
                if result is not None:
                    # result_array = list(
                    #     map(float if self._precision else int, result.split(","))
                    # )
                    # self._attr_native_value = result_array[0]
                    self._coordinator.async_set_updated_data(self._attr_board_blocks)
                else:
                    self._attr_native_value = None
                    self._coordinator.async_set_updated_data(None)  

            self._attr_native_value = result
            self._attr_available = self._attr_native_value is not None
            self.async_write_ha_state()

            _LOGGER.debug( "async_update (%d) '%s' slave:'%s'::%s data:'%s' result:'%s'", 
                round(time.perf_counter()-start_time, 2), self._attr_board, self._slave, str(self._slave_count),
                str(sensor_data.registers if sensor_data.registers else sensor_data.bits),  str(result))
            self._update_lock_flag = False


    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set switch on."""
        await self.async_turn(self.command_on)

class SlaveModbusSwitch(
    CoordinatorEntity[DataUpdateCoordinator[list[int] | None]],
    BoardsBaseSlaveSwitch,
    SwitchEntity,
):
    """Modbus slave register sensor."""
    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        coordinator: DataUpdateCoordinator[list[int] | None],
        entry: dict[str, Any],
        idx: int,
        internal_switch: dict[str, Any],
    ) -> None:
        BoardsBaseSlaveSwitch.__init__(self, hass, hub, entry, Platform.SWITCH, internal_switch.get(CONF_NAME))
        
        self._slave_count = idx
        # self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._attr_name =  internal_switch.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_switch.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + self._attr_sensor_name + ' id ' + str(self._slave)
        ).replace(" ", "_")

        self._attr_manufacturer = self._attr_metadata[ 0 ]
        self._attr_model = self._attr_metadata[ 1 ]

        if internal_switch.get(CONF_REVERSE):
            old = self.command_on
            self.command_on = self._command_off
            self._command_off = old
            old = self._state_on
            self._state_on = self._state_off
            self._state_off = old

        super().__init__(coordinator)

    def _decode_state(self, sensor_data) -> True | False | None:
        result = None

        if sensor_data.registers:
            result_data = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[SwitchRegIdx.BLOCK_DATA_NDX],
                DataType.INT16,
                1,
                0,
            )
        elif sensor_data.bits:
            result_data = sensor_data.bits[self._attr_sensor_registers[SwitchRegIdx.BLOCK_DATA_NDX]]

        if result_data is None:
            return None

        if result_data == self._state_on:
            result = True
        elif result_data == self._state_off:
            result = False

        return result
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        data: dict[str, Any] = { 
            CONF_SLAVE : self._slave,
            "coordinated slave id" : self._slave_count,
        }
        if self._attr_manufacturer:
            data[ "manufacturer" ] = self._attr_manufacturer
        if self._attr_model:
            data[ "model" ] = self._attr_model
        if len(self._attr_sensor_registers) > SwitchRegIdx.GUIDE:
            data[ "guide" ] = self._attr_sensor_registers[SwitchRegIdx.GUIDE]

        return data
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _attr_board_blocks = self.coordinator.data

        if _attr_board_blocks:
            sensor_data = _attr_board_blocks[self._attr_sensor_registers[SwitchRegIdx.BLOCK_NAME]]

            result = self._decode_state(sensor_data)

            if result is None:
                self._attr_available = False
            elif result:
                self._attr_available = True
                self._attr_is_on = True
            else:
                self._attr_available = True
                self._attr_is_on = False

            self._attr_native_value = result
            self._attr_available = self._attr_native_value is not None

            self.async_write_ha_state()
            _LOGGER.debug( "_handle_coordinator_update '%s' slave:'%s'::%s data:'%s' result:'%s'", 
                              self._attr_board, self._slave, str(self._slave_count),
                              str(sensor_data.registers if sensor_data.registers else sensor_data.bits), str(result))
        else:
            self._attr_native_value = None

        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set switch on."""
        await self.async_turn(self.command_on)