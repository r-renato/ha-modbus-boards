# binary_sensor.py
from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, ModbusHub
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import (
    CONF_BINARY_SENSORS,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TYPE,
    CONF_SLAVE,
    Platform,
)

from .helpers.base_entity_class import BaseEntityClass

from .controller.coordinator import ModbusCoordinator

from .const import CONF_BOARD, CONF_ENTITY_CONSTRAINT, COORDINATORS, DOMAIN

from .helpers.utils import slugify
from .helpers.logger import log_info

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup dei binary_sensor per una config entry."""

    # Se in __init__.py hai salvato qualcosa in hass.data[DOMAIN][entry.entry_id]
    # lo recuperi qui (es: client Modbus, coordinator, ecc.)
    # integration_data: dict[str, Any] = hass.data[DOMAIN][entry.entry_id]

    entities: list[DrpModbusBinarySensor] = []

    domain_store = hass.data.setdefault(DOMAIN, {})
    gateway_name = entry.data.get(CONF_NAME)
    coordinator: ModbusCoordinator = domain_store.setdefault(COORDINATORS, {})[gateway_name]

    modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})
    modbus_hub: ModbusHub = modbus_store[slugify(f"{entry.data.get(CONF_TYPE)} {entry.data.get(CONF_HOST)} {entry.data.get(CONF_PORT)}")]

    # La struttura è quella che hai nel log:
    # entry.data["devices"] -> lista di device
    # ogni device ha "binary_sensors": [...]
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

        for binary_sensor_conf in device_conf.get(CONF_BINARY_SENSORS, []):
            entities.append(
                DrpModbusBinarySensor(
                    hass=hass,
                    modbus_hub=modbus_hub,
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    board=board,
                    board_name=board_name,
                    slave=slave,
                    entity_constraint=entity_constraint,
                    config=binary_sensor_conf,
                    # device_name=device_name,
                    # device_function=bs_conf["device_function"],
                    # name=bs_conf["name"],
                    # unique_id=bs_conf["unique_id"],
                )
            )

    if len(entities) > 0:
        async_add_entities(entities)

    log_info(
        _LOGGER,
        "setup for entry '%s' completed. It's set up %s binary_sensor.",
        entry.entry_id,
        len(entities),
    )

class DrpModbusBinarySensor(BaseEntityClass, BinarySensorEntity):
    """Esempio di entity per un coil/bit Modbus."""

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
        config: dict[str, Any]
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
            Platform.BINARY_SENSOR,
        )

        self._attr_is_on: bool | None = None

        log_info(_LOGGER, "(board=%s, slave=%s, function=%s) initialized.", self._board, self._slave, self._device_function)
        
    # @property
    # def available(self) -> bool:
    #     return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool | None:
        return self._attr_is_on
    
    @property
    def device_info(self) -> DeviceInfo:
        """Metadati del dispositivo per raggruppare le entity nel pannello Dispositivi."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=self._board_definition.metadata.name,
            manufacturer=self._board_definition.metadata.manufacturer,
            model=self._board_definition.metadata.model,
            # sw_version=str(INTEGRATION_VERSION),
        )
    
    @property
    def extra_state_attributes(self):
        """Return the extra state attributes of the device."""
        data: dict[str, Any] = self._extra_state_attributes

        if self._register_function is not None:
            if self._register_function.description is not None:
                data["description"] = self._register_function.description
                
        return data
    
    # async def async_update(self) -> None:
    #     """Leggi il valore dal Modbus in base a device_function.

    #     Qui dentro usi integration_data (es. client Modbus o coordinator)
    #     e una mappatura device_function -> indirizzo registro/coil.
    #     """
    #     # TODO: mappare self._device_function su indirizzo/tipo registro
    #     # result = await client.read_coils(...)

    #     # Esempio fittizio:
    #     # self._attr_is_on = bool(result)


    # def _handle_coordinator_update_cccc(self) -> None:
    #     """Aggiorna lo stato in base ai dati letti dal ModbusCoordinator."""
    #     # I dati grezzi per tutte le aree sono in hass.data[DOMAIN][DEVICE_AREAS_DATA]
    #     modbus_registers_response: ModbusRegistersResponse | None = get_stored_board_data_area(
    #         hass=self._hass,
    #         key=self._board_data_area_key,
    #     )

    #     if modbus_registers_response is None:
    #         # Nessun dato ancora disponibile per quest'area
    #         self._attr_is_on = None
    #         # Scrive comunque lo stato (rimane unknown)
    #         self.async_write_ha_state()
    #         return

    #     try:
    #         if not self._register_function:
    #             # Se non ho una register_function valida, non posso decodificare
    #             self._attr_is_on = None
    #             self.async_write_ha_state()
    #             return

    #         address = cast(int, self._register_function.address)
    #         modbus_response = modbus_registers_response.registers_response

    #         value = get_value_from_stored_board_data_area(
    #             modbus_response=modbus_response,
    #             address=address,
    #             datatype=self._data_type,
    #         )
    #         self._attr_is_on = bool(value)

    #         _LOGGER.debug(
    #             "'%s' (key=%s, addr=%s): raw=%s -> is_on=%s",
    #             self._attr_name,
    #             self._board_data_area_key,
    #             address,
    #             value,
    #             self._attr_is_on,
    #         )
    #     except Exception as err:
    #         _LOGGER.debug(
    #             "Impossibile decodificare dati per '%s' (key=%s): %s",
    #             self._attr_unique_id,
    #             self._board_data_area_key,
    #             err,
    #         )
    #         self._attr_is_on = None

    #     # 👉 QUI è il pezzo mancante
    #     self.async_write_ha_state()
    #     # in alternativa:
    #     # super()._handle_coordinator_update()


    def _handle_coordinator_update(self) -> None:
        """Aggiorna lo stato in base ai dati letti dal ModbusCoordinator."""

        self._read_value_from_stored_register(Platform.BINARY_SENSOR)
        # value = self._read_modbus_register(Platform.BINARY_SENSOR)

        # if value is None:
        #     self._attr_is_on = None
        #     self._attr_available = False
        # else:
        #     self._attr_is_on = bool(value)
        #     self._attr_available = True

        # self.async_write_ha_state()
