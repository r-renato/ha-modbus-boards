#
from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.components.modbus.const import (
    DataType,
)
# from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.modbus.modbus import ModbusHub

from homeassistant.const import (
    CONF_NAME,
    CONF_OFFSET,
    CONF_UNIQUE_ID,
    Platform,
)

from ..const import CONF_DEVICE_FUNCTION, DOMAIN, INTEGRATION_NAME
from ..domain.boards import (
    BoardDefinition,
    ModbusRegistersResponse,
    RegisterFunction,
    RegisterFunctionRead,
    RegisterFunctionWrite,
)
from .boards import (
    apply_register_read_transform,
    gen_board_data_area_key,
    get_board_definition,
    get_board_register_function,
    get_stored_board_data_area,
    get_value_from_modbus_response,
    transform_from_modbus_raw_value,
)
from ..controller.coordinator import ModbusCoordinator

from .utils import slugify
from .logger import log_debug, log_exception, log_warning

_LOGGER = logging.getLogger(__name__)

class BaseEntityClass(CoordinatorEntity[ModbusCoordinator], Entity):
    """..."""
    def __init__(
        self,
        hass: HomeAssistant,
        modbus_hub: ModbusHub,
        coordinator: ModbusCoordinator,
        board: str,
        board_name: str,
        slave: int,
        entity_constraint: str,
        entry_id: str,
        config: dict[str, Any],
        platform: Platform,
    ) -> None:
        super().__init__(coordinator)

        self._hass = hass
        self._modbus_hub = modbus_hub
        self._coordinator = coordinator
        self._config = config
        self._entry_id = entry_id

        self._board = board
        self._board_descr = board_name
        self._slave = slave
        self._entity_constraint = entity_constraint

        self._attr_name = self._config.get(CONF_NAME)
        self._attr_unique_id = slugify(
            self._config.get(
                CONF_UNIQUE_ID,
                f"{self._board} slave {self._slave} {self._attr_name}",
            )
        )

        self._device_function: str = self._config.get(CONF_DEVICE_FUNCTION, "")

        if len(self._device_function) == 0:
            log_warning(
                _LOGGER,
                "(board=%s, slave=%s, function=%s)",
                board, slave, self._device_function
            )
            raise ValueError("Required attribute 'device_function' in config")

        self._board_definition: BoardDefinition = get_board_definition(self._board)
        register_function: RegisterFunction | None = get_board_register_function(
            self._board,
            platform,
            self._device_function,
        )

        if register_function is None:
            log_warning(
                _LOGGER,
                "(platform=%s, board=%s, slave=%s, function=%s) Undefined RegisterFunction.",
                platform,
                self._board,
                self._slave,
                self._device_function,
            )
            raise ValueError("Required valid RegisterFunction")

        self._register_function: RegisterFunction = register_function

        if self._register_function.data_type is not None:
            self._data_type = self._register_function.data_type
        else:
            area = self._board_definition.areas[self._register_function.area]
            self._data_type = area.data_type or DataType.UINT16

        self._area_name = self._register_function.area
        self._board_data_area_key = gen_board_data_area_key(
            board=self._board,
            slave=self._slave,
            area_name=self._area_name,
        )

        self._registry_area_shift: int = self._board_definition.areas[self._area_name].registry_area_shift

        self._offset = self._config.get(CONF_OFFSET, 0)

        if self._register_function.state_class is not None:
            self._attr_state_class = self._register_function.state_class

        if self._register_function.device_class is not None:
            self._attr_device_class = self._register_function.device_class

        if self._register_function.unit_of_measurement is not None:
            self._attr_native_unit_of_measurement = self._register_function.unit_of_measurement

        function_read: RegisterFunctionRead | None = self._register_function.function_read
        function_write: RegisterFunctionWrite | None = self._register_function.function_write

        fn_area_def = self._board_definition.areas[self._register_function.area]

        if fn_area_def.mdb_write_function is not None:
            self._modbus_write_function: str = fn_area_def.mdb_write_function

        if function_read is not None:
            state_on = function_read.state_on
            state_off = function_read.state_off
        else:
            state_on = fn_area_def.state_on
            state_off = fn_area_def.state_off

        if function_write:
            cmd_on = function_write.command_on
            cmd_off = function_write.command_off
        else:
            cmd_on = fn_area_def.command_on
            cmd_off = fn_area_def.command_off

        if platform == Platform.SWITCH:
            if state_on is None or state_off is None:
                log_warning(
                    _LOGGER,
                    "(board=%s, slave=%s, function=%s) Undefined state_on/state_off.",
                    self._board,
                    self._slave,
                    self._device_function,
                )
                raise ValueError("Required state_on, state_off for switch")
            
            self._state_on: int = state_on
            self._state_off: int = state_off

            if cmd_on is None or cmd_off is None:
                log_warning(
                    _LOGGER,
                    "(board=%s, slave=%s, function=%s) Undefined command_on/command_off.",
                    self._board,
                    self._slave,
                    self._device_function,
                )
                raise ValueError("Required command_on, command_off for switch.")

            self._command_on: int = cmd_on
            self._command_off: int = cmd_off

            self._reverse_function: bool = False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=self._board_definition.metadata.name,
            manufacturer=self._board_definition.metadata.manufacturer,
            model=self._board_definition.metadata.model
        )
    
    @property
    def _extra_state_attributes(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        data["integration"] = INTEGRATION_NAME
        data["manufacturer"] = self._board_definition.metadata.manufacturer
        data["model"] = self._board_definition.metadata.model
        data["slave"] = self._slave
        data["device_function"] = self._device_function
        data["register_address"] = self._register_function.address

        return data

    def _set_invalid_entity_value(self, platform: Platform):
        if platform in (Platform.NUMBER, Platform.SENSOR):
            self._attr_available = False
            self._attr_native_value = None
        else:
            self._attr_available = False
            self._attr_is_on = None

    def _set_valid_entity_value(self, platform: Platform, value: Any) -> Any:
        if platform in (Platform.NUMBER, Platform.SENSOR):
            self._attr_available = True
            self._attr_native_value = value
            return value
        else:
            self._attr_available = True
            if platform in (Platform.SWITCH) and self._reverse_function:
                self._attr_is_on = not value
            else:
                self._attr_is_on = value
            return self._attr_is_on

    def _read_value_from_stored_register(self, platform: Platform) -> None:
        """Process numeric register value according to data type."""

        constraint_state = None
        if self._entity_constraint is not None:
            constraint_state = self._coordinator.entity_constraint_state(self._entity_constraint)
            if constraint_state is False:
                self._set_invalid_entity_value(platform=platform)
                self.async_write_ha_state()
                return
            
        # Recupera la risposta Modbus per l'area di interesse
        modbus_registers_response: ModbusRegistersResponse | None = get_stored_board_data_area(
            hass=self._hass,
            key=self._board_data_area_key,
        )

        if modbus_registers_response is None or modbus_registers_response.registers_response is None:
            # Nessun dato ancora disponibile per quest'area
            self._set_invalid_entity_value(platform=platform)
            self.async_write_ha_state()
            log_warning(
                _LOGGER,
                "(board=%s, slave=%s, function=%s, constraint_state=%s) No modbus response data.",
                self._board, self._slave, self._device_function, constraint_state
            )
            return

        try:
            address = cast(int, self._register_function.address)
            modbus_response = modbus_registers_response.registers_response

            # Valore grezzo dal blocco di registri
            raw_value = get_value_from_modbus_response(
                modbus_response=modbus_response,
                address=(address + self._registry_area_shift),
                datatype=self._data_type,
            )

            # Applica scale e precision definiti nella funzione di lettura
            value = transform_from_modbus_raw_value(
                raw_value=raw_value, 
                offset_value=self._offset,
                register_area=self._board_definition.areas[self._area_name],
                register_function=self._register_function,
                platform=platform,
            )

            if isinstance(value, str):
                self._set_invalid_entity_value(platform=platform)
                self.async_write_ha_state()
                log_warning(
                    _LOGGER,
                    "(board=%s, slave=%s, function=%s) "
                    "[data key=%s, address=%s] Error transforming raw value=%s: %s",
                    self._board, self._slave, self._device_function,

                    self._board_data_area_key,
                    address,
                    raw_value,
                    value,
                )
                return

            value_end =self._set_valid_entity_value(platform=platform, value=value)

            log_debug(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) "
                "[data key=%s, address=%s] raw=%s, value=%s [reverse=%s, value set=%s]",
                self._board, self._slave, self._device_function,

                self._board_data_area_key,
                address,
                raw_value,
                value,
                getattr(self, "_reverse_function", False),
                value_end,
            )

        except Exception as err:  # noqa: BLE001
            self._set_invalid_entity_value(platform=platform)
            log_exception(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) "
                "Cannot decode data for '%s' [key=%s, modbus response=%s] error: %s",
                self._board, self._slave, self._device_function,

                self._attr_unique_id,
                self._board_data_area_key,
                modbus_registers_response,
                err,
            )

        self.async_write_ha_state()

    def _read_modbus_register(self, platform: Platform) -> Any:
        """Process numeric register value according to data type."""

        # Recupera la risposta Modbus per l'area di interesse
        modbus_registers_response: ModbusRegistersResponse | None = get_stored_board_data_area(
            hass=self._hass,
            key=self._board_data_area_key,
        )

        if modbus_registers_response is None or modbus_registers_response.registers_response is None:
            # Nessun dato ancora disponibile per quest'area
            if platform in (Platform.NUMBER, Platform.SENSOR):
                self._attr_available = False
                self._attr_native_value = None
            else:
                self._attr_is_on = None
                self._attr_available = False

            self.async_write_ha_state()
            log_warning(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) No Modbus response data.",
                self._board, self._slave, self._device_function
            )
            return None

        if not self._register_function:
            # Se non ho una RegisterFunction valida, non posso decodificare
            if platform in (Platform.NUMBER, Platform.SENSOR):
                self._attr_available = False
                self._attr_native_value = None
            else:
                self._attr_is_on = None
                self._attr_available = False
            self.async_write_ha_state()
            log_warning(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) No register function defined for this board.",
                self._board, self._slave, self._device_function
            )
            return None

        try:
            address = cast(int, self._register_function.address)
            modbus_response = modbus_registers_response.registers_response

            # Valore grezzo dal blocco di registri
            raw_value = get_value_from_modbus_response(
                modbus_response=modbus_response,
                address=(address + self._registry_area_shift),
                datatype=self._data_type,
            )

            # Applica scale e precision definiti nella funzione di lettura
            value = apply_register_read_transform(
                raw_value=raw_value,
                offset=self._offset,
                register_function=self._register_function
            )

            log_debug(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) Modbus reading done for "
                "[entity=%s, key=%s] data [addr=%s, raw=%s, native=%s]",
                self._board, self._slave, self._device_function,

                self._attr_name,
                self._board_data_area_key,
                address,
                raw_value,
                value,
            )

        except Exception as err:  # noqa: BLE001
            log_exception(
                _LOGGER,
                "(board=%s, slave=%s, function=%s) "
                "Cannot decode data for '%s' [key=%s] error: %s",
                self._board, self._slave, self._device_function,

                self._attr_unique_id,
                self._board_data_area_key,
                err,
            )
            value = None

        return value




