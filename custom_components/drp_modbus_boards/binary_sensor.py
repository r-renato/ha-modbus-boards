"""Support for Modbus Register sensors."""
from __future__ import annotations

import time
from random import randint
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.sensor import (
    CONF_STATE_CLASS,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_FRIENDLY_NAME,
    CONF_OFFSET,
    CONF_BINARY_SENSORS,
    CONF_SLAVE,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    STATE_ON,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_call_later, async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import get_hub
# from .base_platform import BaseStructPlatform
from .const import CONF_SLAVE_COUNT, CONF_VIRTUAL_COUNT, CONF_DEVICE_ADDRESS, DataType
from .modbus import ModbusHub

from .base_platform import BoardsBaseStructPlatform, DataProcessing
from .boards_const import (
    CONF_BOARD,
    BOARDS,
    METADATA,
    BoardMetadataRegIdx,
    BoardBlockRegIdx,
    BinarySensorRegIdx,
    # BLOCK_NAME,
    # BLOCK_NDX,
    # DATA_TYPE,
    # PRECISION,
    # SCALE,

    # BLK_ADDRESS,
    # BLK_QUANTITY,
    # BLK_FUNCTION,
    # BLK_DATA_TYPE,
    # BLK_STATE_CLOSE,
    # BLK_STATE_OPEN,

    # RBD_BLOCK_NAME,
    # RBD_BLOCK_NDX,
    # RBD_PRECISION,
    # RBD_SCALE,
    # RBD_STATE_CLASS,
    # RBD_DEVICE_CLASS,
    # RBD_UNIT_OF_MEASURE,
    # RWBD_ADDRESS,
    # RWBD_FUNCTION,
    # RWBD_SCALE,
    # RWBD_MIN,
    # RWBD_MAX,
    # RWBD_STEP,
    # RWBD_NMODE,

    # WBD_BLOCK_NAME,
    # WBD_BLOCK_NDX,
    # WBD_ADDRESS,
    # WBD_FUNCTION,
    # WBD_COMMAND_CLOSE,
    # WBD_COMMAND_OPEN,

    # STATE_CLASS,
    # DEVICE_CLASS,
    # UNIT_OF_MEASURE,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Modbus sensors."""

    if discovery_info is None:
        return

    sensors: list[ModbusBinarySensor | SlaveSensor] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for sensor in discovery_info[CONF_BINARY_SENSORS]:
        board_registries = BOARDS[ sensor.get(CONF_BOARD) ][ Platform.BINARY_SENSOR ]
        slave_count = 0
        slaves: list[SlaveSensor] = []
        for int_sensor in sensor.get(CONF_BINARY_SENSORS, None):
            device_name = int_sensor.get(CONF_NAME)
            if device_name in board_registries:
                _LOGGER.debug( "async_setup_platform for board '%s', add binary sensor '%s'", sensor.get(CONF_BOARD), device_name )
                
                if slave_count > 0:
                    slaves.append(await new_sensor.async_setup_slaves(hass, slave_count, sensor, int_sensor))
                else:
                    new_sensor = ModbusBinarySensor(hass, hub, sensor, slave_count, int_sensor)
                slave_count += 1
            else:
                _LOGGER.warning( 'async_setup_platform for board %s, binary sensor %s not exist.', sensor.get(CONF_BOARD), device_name )
        sensors.extend(slaves)
        sensors.append(new_sensor)
    async_add_entities(sensors)


class ModbusBinarySensor(BoardsBaseStructPlatform, RestoreEntity, BinarySensorEntity):
    """Modbus register sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        hub: ModbusHub,
        entry: dict[str, Any],
        slave_count: int,
        internal_sensors: dict[str, Any],
    ) -> None:
        """Initialize the modbus register sensor."""
        super().__init__(hass, hub, entry, Platform.BINARY_SENSOR, internal_sensors.get(CONF_NAME))
        self._slave_count = slave_count
        if slave_count:
            self._count = self._count * (slave_count + 1)
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        self._attr_state_class = entry.get(CONF_STATE_CLASS)
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
# Starting adds
        self._update_lock = asyncio.Lock()
        self._update_lock_flag = False

        self._attr_name =  internal_sensors.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_sensors.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + self._attr_sensor_name + ' id ' + str(self._slave)
        ).replace(" ", "_")

        self._attr_manufacturer = self._attr_metadata[ BoardMetadataRegIdx.MANUFACTURER ]
        self._attr_model = self._attr_metadata[ BoardMetadataRegIdx.MODEL ]
        self._attr_state_class = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_UNIT_OF_MEASURE]

        self._state_on = True
        self._state_off = False

    async def async_setup_slaves(
        self, hass: HomeAssistant, slave_count: int, entry: dict[str, Any], internal_sensor: dict[str, Any]
    ) -> list[SlaveSensor]:
        """Add slaves as needed (1 read for multiple sensors)."""

        # Add a dataCoordinator for each sensor that have slaves
        # this ensures that idx = bit position of value in result
        # polling is done with the base class
        name = self._attr_name if self._attr_name else "modbus_binarysensor"
        if self._coordinator is None:
            self._coordinator = DataUpdateCoordinator(
                hass,
                _LOGGER,
                name=name,
            )

        # slaves: list[SlaveSensor] = []
        # for idx in range(0, slave_count):
        #     slaves.append(SlaveSensor(self._coordinator, idx, entry))
        # return slaves
        return SlaveSensor(self._coordinator, slave_count, entry, internal_sensor)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()
        if state := await self.async_get_last_state():
            self._attr_is_on = state.state == STATE_ON

    def _decode_state(self, sensor_data) -> True | False | None:
        result = None

        if sensor_data.registers:
            result_data = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_NDX],
                DataType.INT16,
                1,
                0,
            )
        elif sensor_data.bits:
            result_data = sensor_data.bits[self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_NDX]]

        if result_data is None:
            return None

        if result_data == self._state_on:
            result = True
        elif result_data == self._state_off:
            result = False

        return result
    
    async def async_update(self, now: datetime | None = None) -> None:
        start_time = time.perf_counter()
        # _LOGGER.debug('async_update %s %s %s', str(self._update_lock_flag), str(self._platform_ready), str(self._state_constraint))
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
            self.async_write_ha_state()
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            return  
        
        async with self._update_lock:
            self._update_lock_flag = True
            self._cancel_call = None
            operation = await self.async_board_read_data(Platform.SENSOR)
            
            sensor_data = self._attr_board_blocks[self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_NAME]]

            if not operation or not sensor_data or not hasattr(sensor_data, "registers"):
                self._attr_available = False
                self._attr_native_value = None
                if self._coordinator:
                    self._coordinator.async_set_updated_data(None)
                self.async_write_ha_state()
                self._update_lock_flag = False
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

class SlaveSensor(
    CoordinatorEntity[DataUpdateCoordinator[list[int] | None]],
    RestoreEntity, 
    BinarySensorEntity
):
    """Modbus slave register sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[list[int] | None],
        idx: int,
        entry: dict[str, Any],
        internal_sensors: dict[str, Any],
    ) -> None:
        """Initialize the Modbus register sensor."""
        self._slave_count = idx
        idx += 1
        self._idx = idx
        self._attr_native_value = None
        self._attr_name = f"{entry[CONF_NAME]} {idx}"
        self._attr_unique_id = entry.get(CONF_UNIQUE_ID)
        if self._attr_unique_id:
            self._attr_unique_id = f"{self._attr_unique_id}_{idx}"
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        self._attr_state_class = entry.get(CONF_STATE_CLASS)
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._attr_available = False

        self._attr_board = entry.get(CONF_BOARD)
        self._attr_metadata = (BOARDS[self._attr_board])[METADATA]
        self._attr_platform_registers = (BOARDS[self._attr_board])[Platform.BINARY_SENSOR]
        self._attr_sensor_registers = self._attr_platform_registers[internal_sensors.get(CONF_NAME)]
        self._slave = entry.get(CONF_SLAVE, None) or entry.get(CONF_DEVICE_ADDRESS, 0)
        self._attr_name =  internal_sensors.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_sensors.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + internal_sensors.get(CONF_NAME) + ' id ' + str(self._slave)
        ).replace(" ", "_")
        self._attr_manufacturer = self._attr_metadata[ BoardMetadataRegIdx.MANUFACTURER ]
        self._attr_model = self._attr_metadata[ BoardMetadataRegIdx.MODEL ]
        self._attr_state_class = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_UNIT_OF_MEASURE]

        self._state_on = True
        self._state_off = False

        super().__init__(coordinator)
    
    async def async_added_to_hass(self) -> None:
        # """Handle entity which will be added."""
        # if state := await self.async_get_last_state():
        #     self._attr_native_value = state.state
        # await super().async_added_to_hass()
        """Handle entity which will be added."""
        if state := await self.async_get_last_state():
            self._attr_is_on = state.state == STATE_ON
            self.async_write_ha_state()
        await super().async_added_to_hass()

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        data: dict[str, Any] = { 
            CONF_SLAVE : self._slave,
            "coordinated slave id" : self._slave_count
        }
        if self._attr_manufacturer:
            data[ "manufacturer" ] = self._attr_manufacturer
        if self._attr_model:
            data[ "model" ] = self._attr_model
        return data
    
    def _decode_state(self, sensor_data) -> True | False | None:
        result = None

        if sensor_data.registers:
            result_data = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_NDX],
                (self._attr_platform_registers[self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_NAME]])[BoardBlockRegIdx.BLOCK_DEF_DATATYPE],
                self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_SCALE],
                self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_PRECISION],
            )
        elif sensor_data.bits:
            result_data = sensor_data.bits[self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_DATA_NDX]]

        if result_data is None:
            return None

        if result_data == self._state_on:
            result = True
        elif result_data == self._state_off:
            result = False

        return result
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _attr_board_blocks = self.coordinator.data

        if _attr_board_blocks:
            sensor_data = _attr_board_blocks[self._attr_sensor_registers[BinarySensorRegIdx.BLOCK_NAME]]

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
                              self._attr_board, str(self._slave), str(self._slave_count),
                              str(sensor_data.registers if sensor_data.registers else sensor_data.bits), str(result))

        else:
            self._attr_native_value = None

        super()._handle_coordinator_update()