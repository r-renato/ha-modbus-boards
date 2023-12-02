"""Support for Modbus Coil and Discrete Input sensors."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    # CONF_STATE_CLASS,
)
from homeassistant.const import (
    CONF_BINARY_SENSORS,
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_FRIENDLY_NAME,
    CONF_SCAN_INTERVAL,
    CONF_UNIQUE_ID,
    STATE_ON,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.event import (
    async_track_state_change_event
)
from . import get_hub
from .base_platform import BasePlatform
from .const import (
    CONF_BOARD,
    CALL_TYPE_COIL,
    CALL_TYPE_DISCRETE,
    CONF_SLAVE_COUNT,
    CONF_VIRTUAL_COUNT,
    CONF_SWITCH_CONSTRAINT,
    STRUCTUREMAP,
    BOARDS_AND_REGISTERS,
    Board,
    BOARD_SENSORS,
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
    """Set up the Modbus binary sensors."""

    if discovery_info is None:
        return

    sensors: list[ModbusBinarySensor | SlaveSensor] = []
    hub = get_hub(hass, discovery_info[CONF_NAME])
    for binary_sensor in discovery_info[CONF_BINARY_SENSORS]:
        board_registries = BOARDS_AND_REGISTERS[ binary_sensor.get(CONF_BOARD) ][ Platform.BINARY_SENSOR ]
        slave_count = binary_sensor.get(CONF_SLAVE_COUNT, None) or binary_sensor.get(
            CONF_VIRTUAL_COUNT, 0
        )
        for int_binary_sensor in binary_sensor.get(CONF_BINARY_SENSORS, None):
            registry = int_binary_sensor.get(CONF_NAME)
            if registry in board_registries:
                _LOGGER.debug( 'async_setup_platform add binary_sensor for board %s and registry %s', binary_sensor.get(CONF_BOARD), registry )
                sensor = ModbusBinarySensor(hub, binary_sensor, slave_count, int_binary_sensor)
                if slave_count > 0:
                    sensors.extend(await sensor.async_setup_slaves(hass, slave_count, binary_sensor))
                sensors.append(sensor)
            else:
                _LOGGER.warning( 'async_setup_platform binary_sensor for board %s, registry %s not exist.', binary_sensor.get(CONF_BOARD), registry )                
    async_add_entities(sensors)


class ModbusBinarySensor(BasePlatform, RestoreEntity, BinarySensorEntity):
    """Modbus binary sensor."""

    def __init__(
            self, 
            hub: ModbusHub, 
            entry: dict[str, Any], 
            slave_count: int, 
            int_binary_sensor: dict[str, Any]
        ) -> None:
        """Initialize the Modbus binary sensor."""
        self._count = slave_count + 1
        self._coordinator: DataUpdateCoordinator[list[int] | None] | None = None
        self._result: list[int] = []
        super().__init__(hub, entry)

        if CONF_SCAN_INTERVAL in int_binary_sensor:
            self._scan_interval = int(int_binary_sensor[CONF_SCAN_INTERVAL])
        self._attr_native_unit_of_measurement = entry.get(CONF_UNIT_OF_MEASUREMENT)
        # self._attr_state_class = entry.get(CONF_STATE_CLASS)

        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._switch_constraint = entry.get(CONF_SWITCH_CONSTRAINT, None)
        if self._switch_constraint is not None:
            self._state_constraint = self.hass.states.get(entry.get( CONF_SWITCH_CONSTRAINT )).state

        self._attr_board = entry.get(CONF_BOARD)
        self._attr_sensor = int_binary_sensor.get(CONF_NAME)
        self._register = BOARDS_AND_REGISTERS[self._attr_board ][ Platform.BINARY_SENSOR ][ self._attr_sensor ]

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

        self._attr_name =  int_binary_sensor.get(CONF_FRIENDLY_NAME, self._attr_name + ' ' + self._register[ 9 ]) 
        self._attr_unique_id = int_binary_sensor.get(CONF_UNIQUE_ID, self._attr_unique_id + '_' + self._register[ 9 ] if self._attr_unique_id else self._attr_name)

        self._attr_manufacturer = self._register[ 10 ]
        self._attr_model = self._register[ 11 ]

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
        if state := await self.async_get_last_state():
            self._attr_is_on = state.state == STATE_ON

        if self._switch_constraint:
            self.async_on_remove(
                    async_track_state_change_event(
                        self.hass, self._switch_constraint, self._async_component_changed
                    )
            )
            _LOGGER.debug( '### async_added_to_hass: %s', str(self._switch_constraint) )

    async def async_update(self, now: datetime | None = None) -> None:
        """Update the state of the sensor."""

        # do not allow multiple active calls to the same platform
        if self._call_active:
            return
        self._call_active = True
        result = await self._hub.async_pb_call(
            self._slave, self._address, self._count, self._input_type
        )
        self._call_active = False
        if result is None:
            if self._lazy_errors:
                self._lazy_errors -= 1
                return
            self._lazy_errors = self._lazy_error_count
            self._attr_available = False
            self._result = []
        else:
            self._lazy_errors = self._lazy_error_count
            self._attr_available = True
            if self._input_type in (CALL_TYPE_COIL, CALL_TYPE_DISCRETE):
                self._result = result.bits
            else:
                self._result = result.registers
            self._attr_is_on = bool(self._result[0] & 1)

        self.async_write_ha_state()
        if self._coordinator:
            self._coordinator.async_set_updated_data(self._result)


class SlaveSensor(
    CoordinatorEntity[DataUpdateCoordinator[list[int] | None]],
    RestoreEntity,
    BinarySensorEntity,
):
    """Modbus slave binary sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[list[int] | None],
        idx: int,
        entry: dict[str, Any],
    ) -> None:
        """Initialize the Modbus binary sensor."""
        idx += 1
        self._attr_name = f"{entry[CONF_NAME]} {idx}"
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._attr_unique_id = entry.get(CONF_UNIQUE_ID)
        if self._attr_unique_id:
            self._attr_unique_id = f"{self._attr_unique_id}_{idx}"
        self._attr_available = False
        self._result_inx = idx
        super().__init__(coordinator)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        if state := await self.async_get_last_state():
            self._attr_is_on = state.state == STATE_ON
            self.async_write_ha_state()
        await super().async_added_to_hass()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        result = self.coordinator.data
        self._attr_is_on = bool(result[self._result_inx] & 1) if result else None
        super()._handle_coordinator_update()