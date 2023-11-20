"""Support for Modbus Register Input Number."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.helpers.event import async_call_later, async_track_time_interval
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.number import (
    NumberEntity,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_DEVICE_CLASS,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_FRIENDLY_NAME,
    CONF_SCAN_INTERVAL,
    Platform,
)
from homeassistant.helpers.event import (
    async_track_state_change_event
)
from . import get_hub
from .base_platform import BaseStructPlatform
from .const import (
    CONF_NUMBERS,
    CONF_SLAVE_COUNT, 
    CONF_VIRTUAL_COUNT,
    CONF_BOARD,
    CONF_SWITCH_CONSTRAINT,
    BOARD_SENSORS,
    MODBUS_DOMAIN as DOMAIN,
    BOARDS_AND_REGISTERS,
    STRUCTUREMAP,
)
from .modbus import ModbusHub

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Read configuration and create Modbus switches."""
    in_numbers = []

    if discovery_info is None:
        return

    for number in discovery_info[CONF_NUMBERS]:
        # _LOGGER.debug( 'async_setup_platform number: ' + str( number ) )
        board_registries = BOARDS_AND_REGISTERS[ number.get(CONF_BOARD) ][ Platform.NUMBER ]

        for int_number in number.get(CONF_NUMBERS, None):
            registry = int_number.get(CONF_NAME)
            if registry in board_registries:
                _LOGGER.debug( 'async_setup_platform add number for board %s and registry %s', number.get(CONF_BOARD), registry )
                hub: ModbusHub = get_hub(hass, discovery_info[CONF_NAME])
                in_numbers.append(ModbusRegisterNumber(hass, hub, number, int_number))
            else:
                _LOGGER.warning( 'async_setup_platform number for board %s, registry %s not exist.', number.get(CONF_BOARD), registry )

    async_add_entities(in_numbers)

class ModbusRegisterNumber(BaseStructPlatform, RestoreEntity, NumberEntity):
    """Modbus register sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        entry: dict[str, Any],
        internal_numbers: dict[str, Any],
    ) -> None:
        """Initialize the modbus register sensor."""
        super().__init__(hub, entry)
        self.hass = hass
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        if CONF_SCAN_INTERVAL in internal_numbers:
            self._scan_interval = int(internal_numbers[CONF_SCAN_INTERVAL])
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        # self._attr_state_class = entry.get(CONF_STATE_CLASS)
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._switch_constraint = entry.get(CONF_SWITCH_CONSTRAINT, None)
        if self._switch_constraint is not None:
            self._state_constraint = self.hass.states.get(entry.get( CONF_SWITCH_CONSTRAINT )).state

        self._attr_board = entry.get(CONF_BOARD)
        self._attr_number = internal_numbers.get(CONF_NAME)
        self._register = BOARDS_AND_REGISTERS[self._attr_board ][ Platform.NUMBER ][ self._attr_number ]
        # self._register = BOARD_SENSORS[ self._attr_board ][ self._attr_sensor ]

# Read data
        self._structure = STRUCTUREMAP[ self._register[ 3 ] ]
        self._address = self._register[ 0 ]
        self._count = self._register[ 1 ]
        self._input_type = self._register[ 2 ]
        self._data_type = self._register[ 3 ]
        self._precision = self._register[ 4 ]
        self._scale = self._register[ 5 ]
# write
        self._write_address = self._register[ 6 ]
        self._write_type = self._register[ 7 ]
        self._write_scale = self._register[ 8 ]

        self._attr_native_min_value = self._register[ 9 ]
        self._attr_native_max_value = self._register[ 10 ]
        self._attr_native_step = self._register[ 11 ]
        self._attr_mode = self._register[ 12 ]

        self._attr_state_class = self._register[ 13 ]
        self._attr_device_class = self._register[ 14 ]
        self._attr_native_unit_of_measurement = self._register[ 15 ]

        self._verify_active = True
        self._verify_delay = 0
        self._verify_address = self._register[ 0 ]
        self._verify_type = self._register[ 2 ]


        self._attr_name =  internal_numbers.get(CONF_FRIENDLY_NAME, self._attr_name + ' ' + self._register[ 16 ]) 
        self._attr_unique_id = internal_numbers.get(CONF_UNIQUE_ID, self._attr_unique_id + '_' + self._register[ 16 ] if self._attr_unique_id else self._attr_name)

        self._attr_manufacturer = self._register[ 17 ]
        self._attr_model = self._register[ 18 ]

    # async def async_added_to_hass(self) -> None:
    #     """Handle entity which will be added."""
    #     await self.async_base_added_to_hass()
    #     state = await self.async_get_last_sensor_data()
    #     if state:
    #         self._attr_native_value = state.native_value

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()

        if self._switch_constraint:
            self.async_on_remove(
                    async_track_state_change_event(
                        self.hass, self._switch_constraint, self._async_component_changed
                    )
            )
            _LOGGER.debug( '### async_added_to_hass: %s', str(self._switch_constraint) )

        # if state := await self.async_get_last_state():
        #     if state.state == STATE_ON:
        #         self._attr_is_on = True
        #     elif state.state == STATE_OFF:
        #         self._attr_is_on = False

    async def async_update(self, now: datetime | None = None) -> None:
        """Update the state of the sensor."""
        _LOGGER.debug( '### async_update number slave:%d, address:%d, %s %s', 
                      self._slave, self._address, self._switch_constraint, str(self._state_constraint) )

        if self._state_constraint != 'on':
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return
                    
        # do not allow multiple active calls to the same platform
        if self._call_active:
            return
        self._call_active = True
        raw_result = await self._hub.async_pb_call(
            self._slave, self._address, self._count, self._input_type
        )
        self._call_active = False

        if raw_result is None:
            # _LOGGER.debug( 'lazy_errors: ', self._lazy_errors )
            if self._lazy_errors:
                self._lazy_errors -= 1
                self._cancel_call = async_call_later(
                    self.hass, timedelta(seconds=1), self.async_update
                )
                return
            self._lazy_errors = self._lazy_error_count
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return
        _LOGGER.debug( '### Number async_update slave:%d, address:%d, write_type:%s, raw:%s', 
             self._slave, self._address, str(self._input_type), str(raw_result.registers) )
        result = self.unpack_structure_result(raw_result.registers)

        _LOGGER.debug( '### Number async_update slave:%d, address:%d, write_type:%s, raw:%s, result:%s', 
             self._slave, self._address, str(self._input_type), str(raw_result.registers), str(result) )
        
        if self._coordinator:
            if result:
                result_array = list(
                    map(float if self._precision else int, result.split(","))
                )
                self._attr_native_value = result_array[0]
                self._coordinator.async_set_updated_data(result_array)
            else:
                self._attr_native_value = None
                self._coordinator.async_set_updated_data(None)
        else:
            self._attr_native_value = result
        self._attr_available = self._attr_native_value is not None
        self._lazy_errors = self._lazy_error_count
        self.async_write_ha_state()


    # def set_native_value(self, value: float) -> None:

    #     _LOGGER.debug( '### Number set_native_value value:%d,', value )
    #     self._attr_native_value = value

    
    async def async_set_modbus_value(self, value: float) -> None:

        address = self._write_address
        value = int(value * self._write_scale)

        _LOGGER.debug( '### Number async_set_modbus_value slave:%d, address:%d, write_type:%s, value:%d,', 
             self._slave, address, str(self._write_type), value )
        
        # builder = BinaryPayloadBuilder(byteorder=Endian.LITTLE, wordorder=Endian.BIG)
        # builder.add_32bit_float(value)
        # payload = builder.build()

        # payload = int(value * 10)
        # client.write_registers(0,payload,count=2,unit= 1,skip_encode = True)
        # _LOGGER.debug( '### Number async_set_modbus_value pre slave:%d, address:%d, write_type:%s, value:%d, payload:%s', 
        #      self._slave, self._address, str(self._write_type), value, str(payload) )
        result = await self._hub.async_pb_call(
            self._slave, self._address, value, self._write_type
        )
        _LOGGER.debug( '### Number async_set_modbus_value post slave:%d, address:%d, write_type:%s, value:%s, result :: %s', 
             self._slave, self._address, str(self._write_type), value, str(result) )
        if result is None:
            self._attr_available = False
            self.async_write_ha_state()
            return
        
        self._attr_available = True
        # if not self._verify_active:
        #     self._attr_is_on = command == self.command_on
        #     self.async_write_ha_state()
        #     return

        if self._verify_delay:
            async_call_later(self.hass, self._verify_delay, self.async_update)
        else:
            await self.async_update()     
    

    # def set_value(self, value: float) -> None:
    #     """Set new value."""   

    #     _LOGGER.debug( '### Number s2 slave:%d, address:%d, write_type:%s, value:%s', 
    #          self._slave, self._address, str(self._register[ 10 ]), value, )

    #     loop = asyncio.get_event_loop()
    #     loop.run_in_executor(None, self.async_set_value, value)
    #     loop.close()


    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( '### Number async_set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )
        # await self.hass.async_add_executor_job(self.set_native_value, value)
        await self.async_set_modbus_value(value)

    def set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( '### Number set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )

