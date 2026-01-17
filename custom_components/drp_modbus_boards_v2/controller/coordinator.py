from __future__ import annotations

from datetime import timedelta
from typing import Any, Callable, Optional
import logging

from homeassistant.core import HomeAssistant, State, Event, EventStateChangedData, callback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TYPE,
    EVENT_HOMEASSISTANT_STARTED,
    STATE_ON,
)
from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, ModbusHub
from homeassistant.exceptions import ConfigEntryNotReady

from ..helpers.ha import entity_state

from ..domain.enums import Board, RegisterAreaName

from ..helpers.boards import gen_board_data_area_key, get_board_definition, store_board_data_area
from ..helpers.modbus import async_modbus_read_area
from ..helpers.config_entries import build_runtime_schema, subscribe_entity_state_changes
from ..helpers.logger import log_debug, log_exception, log_info, log_warning
from ..helpers.utils import slugify

from ..domain.boards import BoardDefinition, RegisterArea
from ..domain.models.runtime_schema import RuntimeEntryConfig
from ..const import DEFAULT_HUB, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ModbusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordina letture Modbus (batch-friendly) e distribuisce i risultati alle entità.

    `requests_builder` deve restituire una lista di DataSpec raggruppabili. La coordinata idempotente di
    aggiornamento legge tutti i gruppi e restituisce un dizionario {key: value_decodificato}.
    Le entità consumano la key che le riguarda.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        config_type: dict[str, Any],
    ) -> None:
        self._hass = hass
        self._config_type = config_type

        self._name = config_type.get(CONF_NAME, DEFAULT_HUB)
        self._connection_type = config_type.get(CONF_TYPE)
        self._host = config_type.get(CONF_HOST)
        self._port = config_type.get(CONF_PORT)

        modbus_hub_key = slugify(f"{self._connection_type} {self._host} {self._port}")

        domain_store = hass.data.setdefault(DOMAIN, {})
        modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})

        # Recupera l'hub Modbus dal nostro store; se non c'è, l'entry non è pronta
        if modbus_hub_key not in modbus_store:
            raise ConfigEntryNotReady(
                f"Modbus hub '{modbus_hub_key}' non pronto (chiave non trovata in modbus_store)"
            )

        self._modbus_hub: ModbusHub = modbus_store[modbus_hub_key]

        self._updt_interval_seconds = timedelta(seconds=30)

        # Inizializza la struttura dati runtime per questa entry
        self._runtime: RuntimeEntryConfig = build_runtime_schema(config_type)

        self._entity_constraint_states: dict[str, State] = {}
        self._entity_constraint_ids: list[str] = []

        super().__init__(
            hass,
            _LOGGER,
            name=slugify(f"{DOMAIN}-{self._name}-coordinator"),
            update_interval=self._updt_interval_seconds,  # loop SLOW
        )

        for device_config in self._runtime.devices:
            constraint = device_config.entity_constraint

            if constraint is not None and constraint not in self._entity_constraint_ids:
                self._entity_constraint_ids.append(constraint)

        self._unsub_state_changes = subscribe_entity_state_changes(
            self._hass, callback=self._entity_changed, entity_ids=self._entity_constraint_ids
        )

        self._unsub_hastarted_event: Optional[Callable[[], None]] = hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, self._async_first_update_entity_constraint_states
        )
        
        log_info(
            _LOGGER,
            "Hub '%s' (object id=%s). Update every %s seconds",
            self._name,
            hex(id(self)),
            self._updt_interval_seconds,
        )

    @callback
    async def _async_first_update_entity_constraint_states(self, event: Event) -> None:
        for entity_id in self._entity_constraint_ids:
            state: State | None = entity_state(self._hass, entity_id=entity_id)

            if not entity_id or state is None:
                continue
            
            self._entity_constraint_states[entity_id] = state

    @callback
    def _entity_changed(self, event: Event[EventStateChangedData]) -> None:
        """Gestisce variazioni di stato sensori/attuatori sottoscritti."""

        entity_id = event.data.get("entity_id")
        new_state: State | None = event.data.get("new_state")
        if not entity_id or new_state is None:
            return

        try:
            self._entity_constraint_states[entity_id] = new_state
            # _LOGGER.debug("State changed: %s -> %s", entity_id, new_state.state)

            # NOTA: non toccare async_set_updated_data qui
            # self.async_set_updated_data({})
            self.async_update_listeners()   # avvisa le entity senza resettare l’interval
        except Exception as ex:  # estrema difesa: non far mai esplodere il job
            log_exception(
                _LOGGER,
                "State change for entity id=%s is ignored. Error %s",
                entity_id, ex
            )

    async def async_config_entry_first_refresh(self) -> None:
        """Primo refresh: usa la semantica standard di DataUpdateCoordinator.

        Se `_async_update_data` solleva UpdateFailed, verrà propagato come
        ConfigEntryNotReady e Home Assistant riproverà a configurare l'entry.
        """
        # log_debug(_LOGGER, "Starting First refresh")
        await super().async_config_entry_first_refresh()

    def entity_constraint_state(self, entity_constraint_id: str) -> bool | None:
        constraint_state: State | None = None
        if entity_constraint_id is not None:
            constraint_state = self._entity_constraint_states.get(entity_constraint_id, None)

        if constraint_state is None:
            return None
    
        return (constraint_state.state == STATE_ON)

    async def async_read_register_data(
        self,
        board: Board,
        slave: int,
        register_area: RegisterArea,
        area: RegisterAreaName | str,
        entity_constraint_id: str | None = None
    ) -> bool | str:
        try:
            constraint_state: State | None = None
            if entity_constraint_id is not None:
                constraint_state = self._entity_constraint_states.get(entity_constraint_id, None)

            response = None
            if constraint_state is None or (constraint_state.state == STATE_ON):
                response = await async_modbus_read_area(
                    modbus=self._modbus_hub,
                    slave=slave,
                    register_area=register_area,
                )

            key = gen_board_data_area_key(board=board, slave=slave, area_name=RegisterAreaName(area))
            store_board_data_area(hass=self._hass, data=response, key=key)

            log_debug(
                _LOGGER,
                "(board=%s, slave=%s) stored [data key=%s, response=%s] "
                "[constraint id=%s, state=%s]",
                board,
                slave,
                key,
                response,
                entity_constraint_id,
                (constraint_state.state if constraint_state else None)
            )

        except Exception as err:  # noqa: BLE001
            board_definition: BoardDefinition = get_board_definition(board=board)
            msg = (
                f"Modbus error reading area '{RegisterAreaName(area)}' "
                f"(board={board_definition.metadata}, slave={slave}, register_area={register_area}): {err}"
            )
            return msg

        return True

    # async def _async_update_datacccccc(self) -> dict[str, Any]:
    #     """Loop SLOW: raccoglie sensori, calcola grandezze derivate e aggiorna lo snapshot.

    #     - Se almeno una lettura ha successo -> last_update_success = True
    #       (entity disponibili, anche se alcune aree possono restare stale/None).
    #     - Se tutte le letture falliscono -> UpdateFailed -> entity unavailable.
    #     """

    #     had_success = False
    #     errors: list[str] = []

    #     for device_config in self._runtime.devices:
    #         board = device_config.board
    #         slave = device_config.slave

    #         constraint_state: State | None = None
    #         entity_constraint_id = device_config.entity_constraint
    #         if entity_constraint_id is not None:
    #             constraint_state = self._entity_constraint_states.get(entity_constraint_id, None)

    #         board_definition: BoardDefinition = get_board_definition(board=board)

    #         for area, register_area in board_definition.areas.items():
    #             try:
    #                 if constraint_state is None or (constraint_state.state == STATE_ON):
    #                     response = await async_modbus_read_area(
    #                         modbus=self._modbus_hub,
    #                         slave=slave,
    #                         register_area=register_area,
    #                     )
    #                 else:
    #                     response = None

    #                 key = gen_board_data_area_key(board=board, slave=slave, area_name=area)
    #                 store_board_data_area(hass=self._hass, data=response, key=key)
                    
    #                 log_debug(
    #                     _LOGGER, 
    #                     "stored for ('%s' %s) %s - %s", key, response, entity_constraint_id, constraint_state if constraint_state else None)

    #                 had_success = True

    #             except Exception as err:  # noqa: BLE001
    #                 msg = (
    #                     f"Errore Modbus leggendo area '{area}' "
    #                     f"(board={board_definition.metadata}, slave={slave}, register_area={register_area}): {err}"
    #                 )
    #                 errors.append(msg)
    #                 # Continuiamo con le altre aree invece di fallire subito
    #                 continue

    #         # log_debug(
    #         #     _LOGGER,
    #         #     "Coordinator '%s' '%s' (board=%s, slave=%s) %s",
    #         #     hex(id(self)),
    #         #     self._name,
    #         #     board,
    #         #     slave,
    #         #     board_definition.areas.items(),
    #         #     # self._hass.data.setdefault(DOMAIN, {}).setdefault(DEVICE_AREAS_DATA, {}).keys(),
    #         # )

    #     if not had_success:
    #         # Nessuna lettura è andata a buon fine → consideriamo l'update fallito
    #         raise UpdateFailed(
    #             "Tutte le letture Modbus sono fallite: " + " | ".join(errors)
    #         )

    #     if len(errors) > 0:
    #         log_warning(_LOGGER, "Modbus read exceptions %s", msg)

    #     # I dati usati dalle entity sono in hass.data[DOMAIN][DEVICE_AREAS_DATA]
    #     return {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Loop SLOW: raccoglie sensori, calcola grandezze derivate e aggiorna lo snapshot.

        - Se almeno una lettura ha successo -> last_update_success = True
          (entity disponibili, anche se alcune aree possono restare stale/None).
        - Se tutte le letture falliscono -> UpdateFailed -> entity unavailable.
        """

        had_success = False
        errors: list[str] = []

        for device_config in self._runtime.devices:
            board = device_config.board
            slave = device_config.slave

            board_definition: BoardDefinition = get_board_definition(board=board)

            for area, register_area in board_definition.areas.items():
                register_result = await self.async_read_register_data(
                    board=board,
                    slave=slave,
                    register_area=register_area,
                    area=RegisterAreaName(area),
                    entity_constraint_id=device_config.entity_constraint
                )

                
                if isinstance(register_result, str):
                    errors.append(register_result)
                else:
                    had_success = True

        if not had_success:
            # Nessuna lettura è andata a buon fine → consideriamo l'update fallito
            raise UpdateFailed(
                "All Modbus read operations failed: " + " | ".join(errors)
            )

        if len(errors) > 0:
            log_warning(
                _LOGGER,
                "Some Modbus read operations failed " + " | ".join(errors)
            )

        # I dati usati dalle entity sono in hass.data[DOMAIN][DEVICE_AREAS_DATA]
        return {}


