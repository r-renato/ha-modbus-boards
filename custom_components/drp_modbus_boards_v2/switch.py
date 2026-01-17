# switch.py
from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, ModbusHub
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TYPE,
    CONF_SWITCHES,
    CONF_SLAVE,
    Platform,
)

from .helpers.boards import get_board

from .helpers.base_entity_class import BaseEntityClass

from .helpers.modbus import async_modbus_write_function

from .controller.coordinator import ModbusCoordinator

from .const import (
    CONF_BOARD,
    CONF_DEVICES,
    CONF_ENTITY_CONSTRAINT,
    CONF_REVERSE,
    COORDINATORS,
    DOMAIN,
)
from .helpers.utils import slugify
from .helpers.logger import log_exception, log_info, log_debug, log_warning


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup degli switch per una config entry Modbus."""

    entities: list[DrpModbusSwitch] = []

    domain_store = hass.data.setdefault(DOMAIN, {})
    gateway_name = entry.data.get(CONF_NAME)
    coordinator: ModbusCoordinator = domain_store.setdefault(COORDINATORS, {})[gateway_name]

    modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})
    modbus_hub: ModbusHub = modbus_store[slugify(f"{entry.data.get(CONF_TYPE)} {entry.data.get(CONF_HOST)} {entry.data.get(CONF_PORT)}")]

    # entry.data["devices"] -> lista di device
    # ogni device ha "switches": [...]
    for device_conf in entry.data.get(CONF_DEVICES, []):
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

        for switch_conf in device_conf.get(CONF_SWITCHES, []):
            entities.append(
                DrpModbusSwitch(
                    hass=hass,
                    modbus_hub=modbus_hub,
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    board=board,
                    board_name=board_name,
                    slave=slave,
                    entity_constraint=entity_constraint,
                    config=switch_conf,
                )
            )

    if entities:
        async_add_entities(entities)

    log_info(
        _LOGGER,
        "setup for entry '%s' completed. It's set up %s switch.",
        entry.entry_id,
        len(entities),
    )

class DrpModbusSwitch(BaseEntityClass, SwitchEntity):
    """Entity switch Modbus basata su DataUpdateCoordinator.

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
            Platform.SWITCH,
        )

        self._reverse_function: bool = self._config.get(CONF_REVERSE, False)

        # function_write: RegisterFunctionWrite | None = self._register_function.function_write
        # function_read: RegisterFunctionRead | None = self._register_function.function_read

        # fn_area_def = self._board_definition.areas[self._register_function.area]

        # if function_write:
        #     cmd_on = function_write.command_on
        #     cmd_off = function_write.command_off
        # else:
        #     cmd_on = fn_area_def.command_on
        #     cmd_off = fn_area_def.command_off

        # if cmd_on is None or cmd_off is None or fn_area_def.mdb_write_function is None:
        #     log_warning(
        #         _LOGGER,
        #         "[switch] (board=%s, slave=%s, func=%s) missing command_on/command_off or mdb_write_function.",
        #         self._board,
        #         self._slave,
        #         self._device_function,
        #     )
        #     raise ValueError("Required command_on, command_off and mdb_write_function for switch")

        # self._modbud_write_function: str = fn_area_def.mdb_write_function

        # self._command_on: int = cmd_on
        # self._command_off: int = cmd_off

        # if function_read:
        #     state_on = function_read.state_on
        #     state_off = function_read.state_off
        # else:
        #     state_on = fn_area_def.state_on
        #     state_off = fn_area_def.state_off

        # if state_on is None or state_off is None:
        #     log_warning(
        #         _LOGGER,
        #         "[switch] (board=%s, slave=%s, func=%s) missing state_on/state_off.",
        #         self._board,
        #         self._slave,
        #         self._device_function,
        #     )
        #     raise ValueError("Required state_on, state_off for switch")

        # self._state_on: int = state_on
        # self._state_off: int = state_off

        # Valore nativo del sensore
        self._attr_is_on: bool | None = None

        log_info(_LOGGER, "(board=%s, slave=%s, function=%s) initialized.", self._board, self._slave, self._device_function)

    # ---------------------------------------------------------------------
    # Metadati del device per raggruppare le entity nel pannello Dispositivi
    # ---------------------------------------------------------------------

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data: dict[str, Any] = self._extra_state_attributes
        data["reverse"] = self._reverse_function

        if self._register_function is not None:
            if self._register_function.description is not None:
                data["description"] = self._register_function.description
                
        return data

    # ------------------------------------------------------------------
    # Comandi ON / OFF
    # ------------------------------------------------------------------
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Esegue il comando Modbus per accendere lo switch."""
        await self._async_write_switch_state(turn=True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Esegue il comando Modbus per spegnere lo switch."""
        await self._async_write_switch_state(turn=False)

    async def _async_write_switch_state(self, turn: bool) -> None:
        """Invia il comando Modbus ON/OFF usando RegisterFunction/Area.

        Il parametro 'turn' rappresenta lo stato LOGICO desiderato del CARICO:
        - turn=True  -> carico acceso
        - turn=False -> carico spento

        La variabile 'reverse' indica se il cablaggio/logica è invertita:
        - reverse=False -> carico e bobina hanno la stessa logica (tipicamente contatto NO)
        - reverse=True  -> carico ON quando la bobina è OFF (tipicamente contatto NC)
        """

        # Valore numerico attuale letto dal registro (stato della BOBINA)
        current_raw_state = self._read_modbus_register(Platform.SWITCH)

        # Determino lo stato attuale della bobina a partire da state_on/state_off
        current_coil: bool | None
        if current_raw_state is None:
            current_coil = None
        elif current_raw_state == self._state_on:
            current_coil = True
        elif current_raw_state == self._state_off:
            current_coil = False
        else:
            # Valore inatteso: non so se la bobina è ON o OFF
            current_coil = None
            log_warning(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) Unexpected value while reading: "
                "raw=%s (valid values: state_on=%s, state_off=%s)",
                self._board,
                self._slave,
                self._device_function,
                current_raw_state,
                self._state_on,
                self._state_off,
            )

        # Stato LOGICO desiderato del CARICO (quello che vuole l'utente)
        desired_load_on: bool = turn

        # Stato desiderato della BOBINA in funzione del flag reverse:
        # - reverse=False: bobina ON  -> carico ON
        # - reverse=True : bobina ON  -> carico OFF
        if self._reverse_function:
            desired_coil_on: bool = not desired_load_on
        else:
            desired_coil_on = desired_load_on

        # Se conosco già lo stato della bobina e corrisponde a quello desiderato, non scrivo
        if current_coil is not None and current_coil == desired_coil_on:
            # log_debug(
            #     _LOGGER,
            #     "[switch] skip write (board=%s, slave=%s, func=%s) "
            #     "raw=%s coil=%s load=%s desired_load=%s desired_coil=%s reverse=%s",
            #     self._board,
            #     self._slave,
            #     self._device_function,
            #     current_raw_state,
            #     current_coil,
            #     self._attr_is_on,
            #     desired_load_on,
            #     desired_coil_on,
            #     self._reverse_function,
            # )
            return

        # Scelgo il valore Modbus da scrivere in funzione dello stato desiderato della BOBINA
        if desired_coil_on:
            value: int = self._command_on
        else:
            value = self._command_off

        try:
            prior_attr_is_on = self._attr_is_on

            # log_debug(
            #     _LOGGER,
            #     "[switch] writing (board=%s, slave=%s, func=%s, addr=%s) "
            #     "modbus (fn=%s, raw_current=%s, state_on=%s, state_off=%s, "
            #     "coil_current=%s, coil_desired=%s, load_desired=%s) value=%s reverse=%s",
            #     self._board,
            #     self._slave,
            #     self._device_function,
            #     self._register_function.address,
            #     self._modbus_write_function,
            #     current_raw_state,
            #     self._state_on,
            #     self._state_off,
            #     current_coil,
            #     desired_coil_on,
            #     desired_load_on,
            #     value,
            #     self._reverse_function,
            # )

            write_result = await async_modbus_write_function(
                modbus_hub=self._modbus_hub,
                slave=self._slave,
                register_address=self._register_function.address,
                # board_register=self._board_definition.registers[Platform.SWITCH],
                # board_function=self._device_function,
                value=value,
                use_call=self._modbus_write_function,
            )

            # Aggiorno lo stato LOGICO lato HA in modo ottimistico:
            # voglio che rappresenti SEMPRE il CARICO, non la bobina.
            if self._reverse_function:
                # Se il carico è ON quando la bobina è OFF, allora:
                # - bobina desiderata ON  -> carico OFF
                # - bobina desiderata OFF -> carico ON
                self._attr_is_on = not desired_coil_on
            else:
                # Carico e bobina coincidono
                self._attr_is_on = desired_coil_on

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

            self.async_write_ha_state()

            log_info(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) [addr=%s, value=%s, reverse=%s] Write succeeded "
                "[result=%s, before=%s -> now=%s]",
                self._board,
                self._slave,
                self._device_function,
                self._register_function.address,
                value,
                self._reverse_function,
                write_result,
                prior_attr_is_on,
                self._attr_is_on,
            )

            # Eventuale riallineamento forzato (se vuoi):
            # await self.coordinator.async_request_refresh()

        except Exception as err:  # noqa: BLE001
            log_exception(
                _LOGGER,
                "(board=%s, slave=%s, func=%s) Switch write operation failed: %s",
                self._board,
                self._slave,
                self._device_function,
                err,
            )

    def _handle_coordinator_update(self) -> None:
        """Aggiorna lo stato in base ai dati letti dal ModbusCoordinator."""

        self._read_value_from_stored_register(Platform.SWITCH)
        # value = self._read_modbus_register(Platform.SWITCH)

        # if value is None:
        #     self._attr_is_on = None
        #     self._attr_available = False
        # else:
        #     self._attr_is_on = (value == self._state_on)
        #     self._attr_available = True


        # # rf = self._register_function.function_read
        # # if rf and rf.state_on is not None and rf.state_off is not None:
        # #     if value == rf.state_on:
        # #         self._attr_is_on = True
        # #     elif value == rf.state_off:
        # #         self._attr_is_on = False
        # #     else:
        # #         # valore inatteso -> magari lascio l'ultimo stato o None
        # #         self._attr_is_on = None
        # # else:
        # #     self._attr_is_on = bool(value)

        # if self._attr_is_on is not None:
        #     if self._reverse_function:
        #         self._attr_is_on = not self._attr_is_on

        # log_debug(
        #     _LOGGER,
        #         "(board=%s, slave=%s, func=%s) [addr=%s, data key=%s] Updated [raw=%s, native=%s]",
        #         self._board,
        #         self._slave,
        #         self._device_function,
        #         self._register_function.address,  
        #         self._board_data_area_key,
        #         value,
        #         self._attr_is_on,     
        # )

        # self.async_write_ha_state()
