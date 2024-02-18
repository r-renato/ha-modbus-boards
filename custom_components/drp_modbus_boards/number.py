"""Support for Modbus Register Number."""
from __future__ import annotations

import time
from random import randint
from datetime import datetime, timedelta
import logging
from typing import Any
import asyncio

from homeassistant.core import HomeAssistant, callback
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
from .base_platform import BoardsBaseNumber, BoardsBaseSlaveNumber, DataProcessing
from .boards_const import (
    CONF_BOARD,
    CONF_NUMBERS,
    MODBUS_DOMAIN as DOMAIN,
    BOARDS,
    BoardMetadataRegIdx,
    BoardBlockRegIdx,
    BoardBlockRegIdx,
    NumericRegIdx,
    # METADATA,
    # BLOCK_NAME,
    # BLOCK_NDX,
    # DATA_TYPE,
    # PRECISION,
    # SCALE,
    # BLK_DATA_TYPE,
    # RBD_BLOCK_NAME,
    # RBD_BLOCK_NDX,
    # RBD_PRECISION,
    # RBD_SCALE,
    # RBD_STATE_CLASS,
    # RBD_DEVICE_CLASS,
    # RBD_UNIT_OF_MEASURE,
    # RWBD_MIN,
    # RWBD_MAX,
    # RWBD_STEP,
    # RWBD_NMODE,
    # RWBD_ADDRESS,
    # RWBD_FUNCTION,
    # RWBD_SCALE,
    # CONF_SWITCH_CONSTRAINT,
)

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
    if discovery_info is None:
        return

    numbers: list[ModbusRegisterNumber | SlaveModbusRegisterNumber] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for conf_numbers in discovery_info[CONF_NUMBERS]:
        board_registries = BOARDS[ conf_numbers.get(CONF_BOARD) ][ Platform.NUMBER ]
        slave_count = 0
        slaves: list[SlaveModbusRegisterNumber] = []
        for int_sensor in conf_numbers.get(CONF_NUMBERS, None):
            device_name = int_sensor.get(CONF_NAME)
            if device_name in board_registries:
                _LOGGER.debug( 'async_setup_platform for board %s, add number %s', conf_numbers.get(CONF_BOARD), device_name )
                
                if slave_count > 0:
                    slaves.append(await new_number.async_setup_slaves(hass, slave_count, conf_numbers, int_sensor))
                else:
                    new_number = ModbusRegisterNumber(hass, hub, conf_numbers, slave_count, int_sensor)
                slave_count += 1
            else:
                _LOGGER.warning( 'async_setup_platform for board %s, number %s not exist.', conf_numbers.get(CONF_BOARD), device_name )
        numbers.extend(slaves)
        numbers.append(new_number)
    async_add_entities(numbers)

class ModbusRegisterNumber(
    BoardsBaseNumber, 
    RestoreEntity, 
    NumberEntity
):
    """Modbus register sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        entry: dict[str, Any],
        slave_count: int,
        internal_numbers: dict[str, Any],
    ) -> None:
        """Initialize the modbus register sensor."""
        super().__init__(hass, hub, entry, Platform.NUMBER, internal_numbers.get(CONF_NAME))
        self._slave_count = slave_count
        if slave_count:
            self._count = self._count * (slave_count + 1)
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        # self._attr_state_class = entry.get(CONF_STATE_CLASS)
        # self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
# Starting adds
        self._update_lock = asyncio.Lock()
        self._update_lock_flag = False

        self._attr_name =  internal_numbers.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_numbers.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + self._attr_sensor_name + ' id ' + str(self._slave)
        ).replace(" ", "_")

        self._attr_native_min_value = self._attr_sensor_registers[NumericRegIdx.SLIDER_MIN]
        self._attr_native_max_value = self._attr_sensor_registers[NumericRegIdx.SLIDER_MAX]
        self._attr_native_step = self._attr_sensor_registers[NumericRegIdx.SLIDER_STEP]
        self._attr_mode = self._attr_sensor_registers[NumericRegIdx.SLIDER_MODE]

        self._attr_manufacturer = self._attr_metadata[BoardMetadataRegIdx.MANUFACTURER]
        self._attr_model = self._attr_metadata[BoardMetadataRegIdx.MODEL ]
        self._attr_state_class = self._attr_sensor_registers[NumericRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[NumericRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[NumericRegIdx.BLOCK_UNIT_OF_MEASURE]


    async def async_setup_slaves(
        self, hass: HomeAssistant, slave_count: int, entry: dict[str, Any], internal_sensor: dict[str, Any]
    ) -> list[SlaveModbusRegisterNumber]:
        """Add slaves as needed (1 read for multiple sensors)."""

        # Add a dataCoordinator for each sensor that have slaves
        # this ensures that idx = bit position of value in result
        # polling is done with the base class
        name = self._attr_name if self._attr_name else "modbus_number"
        if self._coordinator is None:
            self._coordinator = DataUpdateCoordinator(
                hass,
                _LOGGER,
                name=name,
            )

        return SlaveModbusRegisterNumber(hass, self._hub, self._coordinator, entry, slave_count, internal_sensor)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()

        # if self._switch_constraint:
        #     self.async_on_remove(
        #             async_track_state_change_event(
        #                 self.hass, self._switch_constraint, self._async_component_changed
        #             )
        #     )
        _LOGGER.debug( 'async_added_to_hass: %s', str(self._switch_constraint) )

    async def async_update(self, now: datetime | None = None) -> None:
        start_time = time.perf_counter()
        if not self._platform_ready:
            self._cancel_call = async_call_later(
                self.hass, timedelta(seconds=randint(30, 60)), self.async_update
            )
            return 
    
        if self._update_lock_flag:
            return
        
        if self._state_constraint != 'on':
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return        

        async with self._update_lock:
            self._update_lock_flag = True
            self._cancel_call = None
            operation = await self.async_board_read_data(Platform.SENSOR)

            sensor_data = self._attr_board_blocks[self._attr_sensor_registers[NumericRegIdx.BLOCK_NAME]]

            if not operation or not sensor_data or not hasattr(sensor_data, "registers"):
                if self._lazy_errors:
                    self._lazy_errors -= 1
                    self._cancel_call = async_call_later(
                        self.hass, timedelta(seconds=1), self.async_update
                    )
                    self._update_lock_flag = False
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
            
            datatype = (self._attr_platform_registers[self._attr_sensor_registers[NumericRegIdx.BLOCK_NAME]])[BoardBlockRegIdx.BLOCK_DEF_DATATYPE]
            if self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_DATATYPE] is not None:
                datatype = self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_DATATYPE]
            
            result = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_NDX],
                datatype,
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_SCALE],
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_PRECISION],
            )

            if self._coordinator is not None:
                if result:
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

            _LOGGER.debug( "async_update (%d) '%s' slave:'%s' data:'%s' result:'%s'", 
                round(time.perf_counter()-start_time, 2), self._attr_board, self._slave, str(sensor_data), str(result))
            self._update_lock_flag = False

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( 'async_set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )
        # await self.hass.async_add_executor_job(self.set_native_value, value)
        await self.async_set_modbus_value(value)

    def set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( 'set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )


class SlaveModbusRegisterNumber(
    CoordinatorEntity[DataUpdateCoordinator[list[int] | None]],
    BoardsBaseSlaveNumber,
    RestoreEntity, 
    NumberEntity,
):
    """Modbus slave register sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        coordinator: DataUpdateCoordinator[list[int] | None],
        entry: dict[str, Any],
        slave_count: int,
        internal_number: dict[str, Any],
    ) -> None:
        BoardsBaseSlaveNumber.__init__(self, hass, hub, entry, Platform.NUMBER, internal_number.get(CONF_NAME))

        self._slave_count = slave_count
        # self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._attr_name =  internal_number.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_number.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + self._attr_sensor_name + ' id ' + str(self._slave)
        ).replace(" ", "_")

        self._attr_manufacturer = self._attr_metadata[ 0 ]
        self._attr_model = self._attr_metadata[ 1 ]

        self._attr_native_min_value = self._attr_sensor_registers[NumericRegIdx.SLIDER_MIN]
        self._attr_native_max_value = self._attr_sensor_registers[NumericRegIdx.SLIDER_MAX]
        self._attr_native_step = self._attr_sensor_registers[NumericRegIdx.SLIDER_STEP]
        self._attr_mode = self._attr_sensor_registers[NumericRegIdx.SLIDER_MODE]

        self._attr_manufacturer = self._attr_metadata[ BoardMetadataRegIdx.MANUFACTURER ]
        self._attr_model = self._attr_metadata[ BoardMetadataRegIdx.MODEL ]
        self._attr_state_class = self._attr_sensor_registers[NumericRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[NumericRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[NumericRegIdx.BLOCK_UNIT_OF_MEASURE]

        super().__init__(coordinator)

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( 'async_set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )
        # await self.hass.async_add_executor_job(self.set_native_value, value)
        await self.async_set_modbus_value(value)

    def set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug( 'set_native_value slave:%d, address:%d, write_type:%s, value:%s', 
             self._slave, self._address, str(self._write_type), value, )
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _attr_board_blocks = self.coordinator.data

        if _attr_board_blocks:
            sensor_data = _attr_board_blocks[self._attr_sensor_registers[NumericRegIdx.BLOCK_NAME]]
            
            datatype = (self._attr_platform_registers[self._attr_sensor_registers[NumericRegIdx.BLOCK_NAME]])[BoardBlockRegIdx.BLOCK_DEF_DATATYPE]
            if self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_DATATYPE] is not None:
                datatype = self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_DATATYPE]

            result = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_NDX],
                datatype,
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_SCALE],
                self._attr_sensor_registers[NumericRegIdx.BLOCK_DATA_PRECISION],
            )
            
            self._attr_native_value = result
            self._attr_available = self._attr_native_value is not None
            self.async_write_ha_state()

            _LOGGER.debug( "_handle_coordinator_update '%s' slave:'%s'::%s data:'%s' datatype: '%s' result:'%s'", 
                              self._attr_board, self._slave, str(self._slave_count),
                              str(sensor_data.registers if sensor_data.registers else sensor_data.bits),
                              str(datatype), str(result))

        super()._handle_coordinator_update()
