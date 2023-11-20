"""Support for Modbus Register sensors."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from homeassistant.components.sensor import (
    CONF_STATE_CLASS,
    RestoreSensor,
    SensorEntity,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_SENSORS,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_FRIENDLY_NAME,
    CONF_SCAN_INTERVAL,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.event import (
    async_track_state_change_event
)
from . import get_hub
from .base_platform import BaseStructPlatform
from .const import (
    CONF_SLAVE_COUNT, 
    CONF_VIRTUAL_COUNT,
    CONF_BOARD,
    CONF_SWITCH_CONSTRAINT,
    Board,
    BOARD_SENSORS,
    MODBUS_DOMAIN as DOMAIN,
    STRUCTUREMAP,
    BOARDS_AND_REGISTERS,
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
    """Set up the Modbus sensors."""

    if discovery_info is None:
        return

    sensors: list[ModbusRegisterSensor | SlaveSensor] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for sensor in discovery_info[CONF_SENSORS]:
        board_registries = BOARDS_AND_REGISTERS[ sensor.get(CONF_BOARD) ][ Platform.SENSOR ]
        slave_count = sensor.get(CONF_SLAVE_COUNT, None) or sensor.get(
            CONF_VIRTUAL_COUNT, 0
        )
        
        for int_sensor in sensor.get(CONF_SENSORS, None):
            registry = int_sensor.get(CONF_NAME)
            if registry in board_registries:
                _LOGGER.debug( 'async_setup_platform add sensor for board %s and registry %s', sensor.get(CONF_BOARD), registry )
                new_sensor = ModbusRegisterSensor(hass, hub, sensor, slave_count, int_sensor)
                if slave_count > 0:
                    sensors.extend(await sensor.async_setup_slaves(hass, slave_count, sensor))
                sensors.append(new_sensor)
            else:
                _LOGGER.warning( 'async_setup_platform sensor for board %s, registry %s not exist.', sensor.get(CONF_BOARD), registry )

    async_add_entities(sensors)


class ModbusRegisterSensor(BaseStructPlatform, RestoreSensor, SensorEntity):
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
        super().__init__(hub, entry)
        self.hass = hass
        if slave_count:
            self._count = self._count * (slave_count + 1)
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        if CONF_SCAN_INTERVAL in internal_sensors:
            self._scan_interval = int(internal_sensors[CONF_SCAN_INTERVAL])
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        self._attr_state_class = entry.get(CONF_STATE_CLASS)
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._switch_constraint = entry.get(CONF_SWITCH_CONSTRAINT, None)
        if self._switch_constraint is not None:
            self._state_constraint = self.hass.states.get(entry.get( CONF_SWITCH_CONSTRAINT )).state

        self._attr_board = entry.get(CONF_BOARD)
        self._attr_sensor = internal_sensors.get(CONF_NAME)
        self._register = BOARDS_AND_REGISTERS[self._attr_board ][ Platform.SENSOR ][ self._attr_sensor ]

        # self._attr_board = entry.get(CONF_BOARD)
        # self._attr_sensor = internal_sensor.get(CONF_NAME)
        # self._register = BOARD_SENSORS[ self._attr_board ][ self._attr_sensor ]

        self._structure = STRUCTUREMAP[ self._register[ 3 ] ]
        self._address = self._register[ 0 ]
        self._count = self._register[ 1 ]
        self._input_type = self._register[ 2 ]
        self._data_type = self._register[ 3 ]
        self._precision = self._register[ 4 ]
        self._scale = self._register[ 5 ]

        self._attr_state_class = self._register[ 6 ]
        self._attr_device_class = self._register[ 7 ]
        self._attr_native_unit_of_measurement = self._register[ 8 ]

        self._attr_name =  internal_sensors.get(CONF_FRIENDLY_NAME, self._attr_name + ' ' + self._register[ 9 ]) 
        self._attr_unique_id = internal_sensors.get(CONF_UNIQUE_ID, self._attr_unique_id + '_' + self._register[ 9 ] if self._attr_unique_id else self._attr_name)

        self._attr_manufacturer = self._register[ 10 ]
        self._attr_model = self._register[ 11 ]

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        assert self.platform.config_entry and self.platform.config_entry.unique_id
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.platform.config_entry.unique_id)},
            manufacturer = self._attr_manufacturer,
            model=self._attr_model,
            name=self.coordinator.name,
        )
    
    async def async_setup_slaves(
        self, hass: HomeAssistant, slave_count: int, entry: dict[str, Any]
    ) -> list[SlaveSensor]:
        """Add slaves as needed (1 read for multiple sensors)."""

        # Add a dataCoordinator for each sensor that have slaves
        # this ensures that idx = bit position of value in result
        # polling is done with the base class
        name = self._attr_name if self._attr_name else "modbus_sensor"
        self._coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=name,
        )

        slaves: list[SlaveSensor] = []
        for idx in range(0, slave_count):
            slaves.append(SlaveSensor(self._coordinator, idx, entry))
        return slaves

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()
        state = await self.async_get_last_sensor_data()
        if state:
            self._attr_native_value = state.native_value

        if self._switch_constraint:
            self.async_on_remove(
                    async_track_state_change_event(
                        self.hass, self._switch_constraint, self._async_component_changed
                    )
            )
            _LOGGER.debug( '### async_added_to_hass: %s', str(self._switch_constraint) )

    async def async_update(self, now: datetime | None = None) -> None:
        """Update the state of the sensor."""
        # _LOGGER.debug( '### async_update: %s', str(self._state_constraint) )
        _LOGGER.debug( '### async_update slave:%d, address:%d, %s %s', 
                      self._slave, self._address, self._switch_constraint, str(self._state_constraint) )
        if self._state_constraint != 'on':
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return            

        # remark "now" is a dummy parameter to avoid problems with
        # async_track_time_interval
        self._cancel_call = None

        # _LOGGER.debug( 'slave: %d, address: %d, count: %d, operation: %s', 
        #               self._slave, self._address, self._count, self._input_type )
        raw_result = await self._hub.async_pb_call(
            self._slave, self._address, self._count, self._input_type
        )
        # raw_result = await self._hub.async_pb_call(
        #     self._slave, self._register[0], self._register[1], self._register[2]
        # )

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

        result = self.unpack_structure_result(raw_result.registers)
        # _LOGGER.debug( "ciao" )
        # _LOGGER.debug( 'input: %s, %s' + str(raw_result.registers), str(result))
        # _LOGGER.debug( '### slave:%d, address:%d, count:%d, operation:%s, raw :: %s, result :: %s', 
            #  self._slave, self._address, self._count, self._input_type, str(raw_result.registers), str(result) )
        if self._attr_board == Board.ELETECHSUP_NT18B07 and str(result) == str(6280.5):
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return

        if self._attr_board == Board.ELETECHSUP_N4DBA06 and (self._attr_sensor == "vin1_ratio" or self._attr_sensor == "vin2_ratio"):
            result = (float(result)-1000)*0.1

        # _LOGGER.debug( '#### slave:%d, address:%d, count:%d, operation:%s, >>result :: %s, %s, %s', 
        #      self._slave, self._address, self._count, self._input_type, type(result), str(result), self._attr_sensor )
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
    ) -> None:
        """Initialize the Modbus register sensor."""
        idx += 1
        self._idx = idx
        self._attr_name = f"{entry[CONF_NAME]} {idx}"
        self._attr_unique_id = entry.get(CONF_UNIQUE_ID)
        if self._attr_unique_id:
            self._attr_unique_id = f"{self._attr_unique_id}_{idx}"
        self._attr_native_unit_of_measurement = "xyz" # entry.get(CONF_UNIT_OF_MEASUREMENT)
        self._attr_state_class = entry.get(CONF_STATE_CLASS)
        self._attr_available = False
        super().__init__(coordinator)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        if state := await self.async_get_last_state():
            self._attr_native_value = state.state
        await super().async_added_to_hass()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        result = self.coordinator.data
        self._attr_native_value = result[self._idx] if result else None
        super()._handle_coordinator_update()