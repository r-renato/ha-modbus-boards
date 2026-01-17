# sensor.py
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, ModbusHub
from homeassistant.components.modbus.const import DataType
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_TYPE,
    CONF_NAME,
    CONF_SLAVE,
    Platform,
)

from .helpers.boards import get_board

from .helpers.modbus import async_modbus_write_function, convert_native_2_register_value, is_int_dtype

from .const import CONF_BOARD, CONF_ENTITY_CONSTRAINT, CONF_NUMBERS, COORDINATORS, DOMAIN
from .controller.coordinator import ModbusCoordinator
from .helpers.base_entity_class import BaseEntityClass
from .helpers.logger import log_debug, log_exception, log_info, log_warning
from .helpers.utils import slugify


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup dei Number per una config entry Modbus."""

    entities: list[DrpModbusNumber] = []

    domain_store = hass.data.setdefault(DOMAIN, {})
    gateway_name = entry.data.get(CONF_NAME)
    coordinator: ModbusCoordinator = domain_store.setdefault(COORDINATORS, {})[gateway_name]

    modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})
    modbus_hub: ModbusHub = modbus_store[slugify(f"{entry.data.get(CONF_TYPE)} {entry.data.get(CONF_HOST)} {entry.data.get(CONF_PORT)}")]

    for device_conf in entry.data.get("devices", []):
        board = device_conf.get(CONF_BOARD)
        board_name = device_conf.get(CONF_NAME)
        slave = device_conf.get(CONF_SLAVE)
        entity_constraint = device_conf.get(CONF_ENTITY_CONSTRAINT)
        
        log_info(
            _LOGGER,
            "(board='%s' slave='%s' board name='%s') setup for entry '%s'.",
            board,
            slave,
            board_name,
            entry.entry_id,
        )

        for number_conf in device_conf.get(CONF_NUMBERS, []):
            entities.append(
                DrpModbusNumber(
                    hass=hass,
                    modbus_hub=modbus_hub,
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    board=board,
                    board_name=board_name,
                    slave=slave,
                    entity_constraint=entity_constraint,
                    config=number_conf,
                )
            )

    if entities:
        async_add_entities(entities)

    log_info(
        _LOGGER,
        "setup for entry '%s' completed. It's set up %s number.",
        entry.entry_id,
        len(entities),
    )

class DrpModbusNumber(BaseEntityClass, NumberEntity):
    """Entity sensore Modbus basata su DataUpdateCoordinator.

    Il valore viene letto dal ModbusCoordinator, che esegue le letture Modbus,
    e decodificato usando la definizione di RegisterFunction della board.
    """

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
    ) -> None:
        super().__init__(
            hass,
            modbus_hub,
            coordinator,
            board,
            board_name,
            slave,
            entity_constraint,
            entry_id,
            config,
            Platform.NUMBER,
        )

        if self._register_function.min is not None:
            self._attr_native_min_value = self._register_function.min

        if self._register_function.max is not None:
            self._attr_native_max_value = self._register_function.max

        if self._register_function.function_write is not None:
            if self._register_function.function_write.step is not None: 
                self._attr_native_step = self._register_function.function_write.step

            if self._register_function.function_write.number_mode is not None:       
                self._attr_mode = self._register_function.function_write.number_mode

            if self._register_function.function_write.scale is not None:
                self._write_scale = self._register_function.function_write.scale

        log_info(_LOGGER, "(board=%s, slave=%s, function=%s) initialized.", self._board, self._slave, self._device_function)

    # ---------------------------------------------------------------------
    # Metadati del device per raggruppare le entity nel pannello Dispositivi
    # ---------------------------------------------------------------------
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data: dict[str, Any] = self._extra_state_attributes

        if self._register_function is not None:
            fr = self._register_function.function_read
            fw = self._register_function.function_write
            if fw is not None and fw.number_mode is not None:
                data["mode"] = fw.number_mode
            if fr is not None and fr.precision is not None:
                data["precision"] = fr.precision
            if self._register_function.min is not None:
                data["min"] = self._register_function.min
            if self._register_function.max is not None:
                data["max"] = self._register_function.max
            if self._register_function.default is not None:
                data["default"] = self._register_function.default
            if self._register_function.description is not None:
                data["description"] = self._register_function.description

        return data
    
    def set_native_value(self, value: float) -> None:
        """Set new value."""
        raise NotImplementedError

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        try:
            prior_attr_native_value = self._attr_native_value

            dtype = self._register_function.data_type or DataType.UINT16

            if not is_int_dtype(dtype):
                log_warning(
                    _LOGGER,
                    "(board=%s, slave=%s, func=%s) Unexpected data type: %s ",
                    self._board,
                    self._slave,
                    self._device_function,
                    dtype,
                )
                raise TypeError(f"async_modbus_write_function accetta solo int, dtype={dtype}")

            write_value = convert_native_2_register_value(
                value=value,
                scale=self._write_scale,
                dtype=dtype,
            )
            
            log_debug(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) [raw=%s, scale=%s, modbus native=%s]",
                self._board,
                self._slave,
                self._device_function,
                value,
                self._write_scale,
                write_value,
            )

            write_result = await async_modbus_write_function(
                modbus_hub=self._modbus_hub,
                slave=self._slave,
                register_address=self._register_function.address,
                # board_register=self._board_definition.registers[Platform.SWITCH],
                # board_function=self._device_function,
                value=write_value,
                use_call=self._modbus_write_function,
            )
            
            self._attr_available = True
            
            fetch_result = await self._coordinator.async_read_register_data(
                board=get_board(self._board),
                slave=self._slave,
                register_area=self._board_definition.areas[self._register_function.area],
                area=self._register_function.area,
                entity_constraint_id=self.entity_id
            )

            if isinstance(fetch_result, str):
                self._attr_available = False
                log_warning(
                    _LOGGER,
                    "(board=%s, slave=%s, func=%s) Modbus read operation error: %s",
                    self._board,
                    self._slave,
                    self._device_function,
                    fetch_result,
                )

            if self._attr_available:
                self._attr_native_value = value

            self.async_write_ha_state()

            log_info(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) [addr=%s, value=%s] Write succeeded "
                "[result=%s, before=%s -> now=%s]",
                self._board,
                self._slave,
                self._device_function,
                self._register_function.address,
                value,
                write_result,
                prior_attr_native_value,
                self._attr_native_value,
            )

        except Exception as err:  # noqa: BLE001
            log_exception(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) Number write operation failed: %s",
                self._board,
                self._slave,
                self._device_function,
                err,
            )
    # ---------------------------------------------------------------------
    # Integrazione con il DataUpdateCoordinator
    # ---------------------------------------------------------------------
    def _handle_coordinator_update(self) -> None:
        """Aggiorna lo stato in base ai dati letti dal ModbusCoordinator."""

        self._read_value_from_stored_register(Platform.NUMBER)

        # value = self._read_modbus_register(Platform.NUMBER)

        # if value is None:
        #     self._attr_native_value = None
        #     self._attr_available = False
        # else:
        #     self._attr_native_value = value
        #     self._attr_available = True

        # self.async_write_ha_state()
