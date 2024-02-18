"""Support for Modbus Register sensors."""
from __future__ import annotations

import time
from random import randint
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Any

from homeassistant.components.sensor import (
    CONF_STATE_CLASS,
    RestoreSensor,
    SensorEntity,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_FRIENDLY_NAME,
    CONF_OFFSET,
    CONF_SENSORS,
    CONF_SLAVE,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
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

from . import get_hub
# from .base_platform import BaseStructPlatform
from .const import CONF_SLAVE_COUNT, CONF_VIRTUAL_COUNT, CONF_DEVICE_ADDRESS
from .modbus import ModbusHub

from .base_platform import BoardsBaseStructPlatform, DataProcessing
from .boards_const import (
    CONF_BOARD,
    BOARDS,
    METADATA,
    BoardMetadataRegIdx,
    BoardBlockRegIdx,
    SensorRegIdx,
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

    sensors: list[ModbusRegisterSensor | SlaveSensor] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for sensor in discovery_info[CONF_SENSORS]:
        board_registries = BOARDS[ sensor.get(CONF_BOARD) ][ Platform.SENSOR ]
        slave_count = 0
        slaves: list[SlaveSensor] = []
        for int_sensor in sensor.get(CONF_SENSORS, None):
            device_name = int_sensor.get(CONF_NAME)
            if device_name in board_registries:
                _LOGGER.debug( "async_setup_platform for board '%s', add sensor '%s'", sensor.get(CONF_BOARD), device_name )
                
                if slave_count > 0:
                    slaves.append(await new_sensor.async_setup_slaves(hass, slave_count, sensor, int_sensor))
                else:
                    new_sensor = ModbusRegisterSensor(hass, hub, sensor, slave_count, int_sensor)
                    slave_count += 1
            else:
                _LOGGER.warning( 'async_setup_platform for board %s, sensor %s not exist.', sensor.get(CONF_BOARD), device_name )
        sensors.extend(slaves)
        sensors.append(new_sensor)
    async_add_entities(sensors)


class ModbusRegisterSensor(BoardsBaseStructPlatform, RestoreSensor, SensorEntity):
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
        super().__init__(hass, hub, entry, Platform.SENSOR, internal_sensors.get(CONF_NAME))
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
        self._attr_state_class = self._attr_sensor_registers[SensorRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[SensorRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[SensorRegIdx.BLOCK_UNIT_OF_MEASURE]

    async def async_setup_slaves(
        self, hass: HomeAssistant, slave_count: int, entry: dict[str, Any], internal_sensor: dict[str, Any]
    ) -> list[SlaveSensor]:
        """Add slaves as needed (1 read for multiple sensors)."""

        # Add a dataCoordinator for each sensor that have slaves
        # this ensures that idx = bit position of value in result
        # polling is done with the base class
        name = self._attr_name if self._attr_name else "modbus_sensor"
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
        state = await self.async_get_last_sensor_data()
        if state:
            self._attr_native_value = state.native_value

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
            
            sensor_data = self._attr_board_blocks[self._attr_sensor_registers[SensorRegIdx.BLOCK_NAME]]

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
                _LOGGER.debug( "async_update (%d) '%s' slave:'%s' Error reading data. (%s)", 
                    round(time.perf_counter()-start_time, 2), self._attr_board, self._slave, str(sensor_data))
                return
            
            result = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_NDX],
                (self._attr_platform_registers[self._attr_sensor_registers[SensorRegIdx.BLOCK_NAME]])[BoardBlockRegIdx.BLOCK_DEF_DATATYPE],
                self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_SCALE],
                self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_PRECISION],
            )

            if self._coordinator:
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
        
    # async def async_update_old(self, now: datetime | None = None) -> None:
    #     """Update the state of the sensor."""
    #     # remark "now" is a dummy parameter to avoid problems with
    #     # async_track_time_interval
    #     self._cancel_call = None
    #     raw_result = await self._hub.async_pb_call(
    #         self._slave, self._address, self._count, self._input_type
    #     )
    #     if raw_result is None:
    #         self._attr_available = False
    #         self._attr_native_value = None
    #         if self._coordinator:
    #             self._coordinator.async_set_updated_data(None)
    #         self.async_write_ha_state()
    #         return

    #     result = self.unpack_structure_result(raw_result.registers)
    #     if self._coordinator:
    #         if result:
    #             result_array = list(
    #                 map(float if self._precision else int, result.split(","))
    #             )
    #             self._attr_native_value = result_array[0]
    #             self._coordinator.async_set_updated_data(result_array)
    #         else:
    #             self._attr_native_value = None
    #             self._coordinator.async_set_updated_data(None)
    #     else:
    #         self._attr_native_value = result
    #     self._attr_available = self._attr_native_value is not None
    #     self.async_write_ha_state()


class SlaveSensor(
    CoordinatorEntity[DataUpdateCoordinator[list[int] | None]],
    RestoreSensor,
    SensorEntity,
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
        self._attr_platform_registers = (BOARDS[self._attr_board])[Platform.SENSOR]
        self._attr_sensor_registers = self._attr_platform_registers[internal_sensors.get(CONF_NAME)]
        self._slave = entry.get(CONF_SLAVE, None) or entry.get(CONF_DEVICE_ADDRESS, 0)
        self._attr_name =  internal_sensors.get(CONF_FRIENDLY_NAME) 
        self._attr_unique_id = internal_sensors.get(
            CONF_UNIQUE_ID,
            self._attr_board + ' ' + internal_sensors.get(CONF_NAME) + ' id ' + str(self._slave)
        ).replace(" ", "_")
        self._attr_manufacturer = self._attr_metadata[ BoardMetadataRegIdx.MANUFACTURER ]
        self._attr_model = self._attr_metadata[ BoardMetadataRegIdx.MODEL ]
        self._attr_state_class = self._attr_sensor_registers[SensorRegIdx.BLOCK_STATE_CLASS]
        self._attr_device_class = self._attr_sensor_registers[SensorRegIdx.BLOCK_DEVICE_CLASS]
        self._attr_native_unit_of_measurement = self._attr_sensor_registers[SensorRegIdx.BLOCK_UNIT_OF_MEASURE]

        self._min_value = None
        self._max_value = None
        self._zero_suppress = None
        self._nan_value = None
        self._offset = entry[CONF_OFFSET]

        super().__init__(coordinator)
    
    async def async_added_to_hass(self) -> None:
        # """Handle entity which will be added."""
        # if state := await self.async_get_last_state():
        #     self._attr_native_value = state.state
        # await super().async_added_to_hass()
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_sensor_data()
        if state:
            self._attr_native_value = state.native_value

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
        return data
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _attr_board_blocks = self.coordinator.data

        if _attr_board_blocks:
            sensor_data = _attr_board_blocks[self._attr_sensor_registers[SensorRegIdx.BLOCK_NAME]]
            # sensor_value = sensor_data.registers[self._attr_sensor_registers[BLOCK_NDX]]
            # result = self._process_raw_value(sensor_value, self._attr_sensor_registers[SCALE], self._attr_sensor_registers[PRECISION])

            result = DataProcessing.unpack_data( 
                    sensor_data.registers,
                    self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_NDX],
                    (self._attr_platform_registers[self._attr_sensor_registers[SensorRegIdx.BLOCK_NAME]])[BoardBlockRegIdx.BLOCK_DEF_DATATYPE],
                    self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_SCALE],
                    self._attr_sensor_registers[SensorRegIdx.BLOCK_DATA_PRECISION],
            )

            _LOGGER.debug( "_handle_coordinator_update '%s' %s", str(sensor_data.registers), str(result))

            # self._attr_native_value = result[self._idx] if result else None
            self._attr_native_value = result
        else:
            self._attr_native_value = None
        super()._handle_coordinator_update()
