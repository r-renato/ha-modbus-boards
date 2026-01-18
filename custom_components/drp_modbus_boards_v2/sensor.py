# sensor.py
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, ModbusHub
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_TYPE,
    CONF_NAME,
    CONF_SENSORS,
    CONF_SLAVE,
    Platform,
)
from .helpers.base_entity_class import BaseEntityClass
from .controller.coordinator import ModbusCoordinator

from .const import (
    CONF_BOARD,
    CONF_ENTITY_CONSTRAINT,
    COORDINATORS,
    DOMAIN,
)
from .helpers.utils import slugify
from .helpers.logger import log_info


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup dei sensori per una config entry Modbus."""

    entities: list[DrpModbusSensor] = []

    domain_store = hass.data.setdefault(DOMAIN, {})
    gateway_name = entry.data.get(CONF_NAME)
    coordinator: ModbusCoordinator = domain_store.setdefault(COORDINATORS, {})[gateway_name]

    modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})
    modbus_hub: ModbusHub = modbus_store[slugify(f"{entry.data.get(CONF_TYPE)} {entry.data.get(CONF_HOST)} {entry.data.get(CONF_PORT)}")]


    # entry.data["devices"] -> lista di device
    # ogni device ha "sensors": [...]
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

        for sensor_conf in device_conf.get(CONF_SENSORS, []):
            entities.append(
                DrpModbusSensor(
                    hass=hass,
                    modbus_hub=modbus_hub,
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    board=board,
                    board_name=board_name,
                    slave=slave,
                    entity_constraint=entity_constraint,
                    config=sensor_conf,
                )
            )

    if entities:
        async_add_entities(entities)

    log_info(
        _LOGGER,
        "setup for entry '%s' completed. It's set up %s sensor.",
        entry.entry_id,
        len(entities),
    )

class DrpModbusSensor(BaseEntityClass, SensorEntity):
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
            Platform.SENSOR,
        )

        # self._hass = hass
        # self._config = config
        # self._entry_id = entry_id

        # self._board = board
        # self._board_descr = board_name
        # self._slave = slave

        # self._attr_name = self._config.get(CONF_NAME)
        # self._attr_unique_id = slugify(
        #     self._config.get(
        #         CONF_UNIQUE_ID,
        #         f"{self._board} slave {self._slave} {self._attr_name}",
        #     )
        # )

        # self._device_function = self._config.get(CONF_DEVICE_FUNCTION, "")
        # log_debug(_LOGGER, "(board=%s, slave=%s, name=%s)", board, slave, board_name, self._device_function)

        # self._board_definition: BoardDefinition = get_board_definition(self._board)
        # self._register_function = get_board_register_function(
        #     self._board,
        #     Platform.SENSOR,
        #     self._device_function,
        # )

        # if self._register_function:
        #     area = self._board_definition.areas[self._register_function.area]
        #     self._data_type = area.data_type or DataType.UINT16
        # else:
        #     self._data_type = DataType.UINT16

        # self._offset = self._config.get(CONF_OFFSET, 0)

        # # Chiave con cui il coordinator salva i dati dell'area in DEVICE_AREAS_DATA
        # area_name = self._register_function.area if self._register_function else ""
        # self._board_data_area_key = gen_board_data_area_key(
        #     board=self._board,
        #     slave=self._slave,
        #     area_name=area_name,
        # )

        # Valore nativo del sensore
        self._attr_native_value: Any | None = None

        # # Metadati dal RegisterFunction, se disponibili
        # if self._register_function is not None:
        #     # Unit, device_class, state_class definiti nella board
        #     if self._register_function.unit_of_measurement is not None:
        #         self._attr_native_unit_of_measurement = (
        #             self._register_function.unit_of_measurement
        #         )

        #     if self._register_function.device_class is not None:
        #         self._attr_device_class = resolve_sensor_device_class(self._register_function.device_class)

        #     if self._register_function.state_class is not None:
        #         self._attr_state_class = self._register_function.state_class

        log_info(_LOGGER, "(board=%s, slave=%s, function=%s) initialized.", self._board, self._slave, self._device_function)

    # ---------------------------------------------------------------------
    # Metadati del device per raggruppare le entity nel pannello Dispositivi
    # ---------------------------------------------------------------------

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data: dict[str, Any] = self._extra_state_attributes

        if self._register_function is not None:
            fr = self._register_function.function_read
            if fr is not None and fr.scale is not None:
                data["scale"] = fr.scale
            if fr is not None and fr.precision is not None:
                data["precision"] = fr.precision
            if self._register_function.min is not None:
                data["min"] = self._register_function.min
            if self._register_function.max is not None:
                data["max"] = self._register_function.max
            if self._register_function.description is not None:
                data["description"] = self._register_function.description

        return data

    def _handle_coordinator_update(self) -> None:
        """Aggiorna lo stato in base ai dati letti dal ModbusCoordinator."""

        self._read_value_from_stored_register(Platform.SENSOR)

        # self.async_write_ha_state()
