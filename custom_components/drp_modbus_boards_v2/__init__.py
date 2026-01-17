"""Support for Modbus."""
from __future__ import annotations

from typing import Any
import logging

from homeassistant.core import HomeAssistant, Event, ServiceCall
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.reload import async_integration_yaml_config
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import ConfigEntryNotReady

from homeassistant.components.modbus.modbus import DATA_MODBUS_HUBS, async_modbus_setup
from homeassistant.components.modbus.const import DOMAIN as MODBUS_DOMAIN
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.validators import check_config

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TYPE,
    SERVICE_RELOAD,
    Platform,
)

from .helpers.utils import slugify

from .helpers.config_entries import build_modbus_ha_config

from .controller.coordinator import ModbusCoordinator
from .helpers.logger import log_debug, log_info, log_warning
from .helpers.ha import ensure_number_in_platforms
from .const import COORDINATORS, DEFAULT_HUB, DOMAIN, CONF_NUMBERS, PLATFORMS

from .domain.models import aermec_hmi080  # noqa: F401
from .domain.models import eneren_rer020i  # noqa: F401
from .domain.models import eastron_sdm120m  # noqa: F401
from .domain.models import eletechsup_10ioa04  # noqa: F401
from .domain.models import eletechsup_n4dba06  # noqa: F401
from .domain.models import eletechsup_nt18b07  # noqa: F401
from .domain.models import eletechsup_r4d3b16  # noqa: F401
from .domain.models import gauselink_th02_pe  # noqa: F401
from .domain.models import xy_mod01_sht20  # noqa: F401
from .domain.models import waveshare_rtu_relay  # noqa: F401

from .domain.schema import (
    CONFIG_SCHEMA,
    BINARY_SENSOR_SCHEMA,
    SENSOR_SCHEMA,
    SWITCH_SCHEMA,
    NUMBER_SCHEMA,
)

_LOGGER = logging.getLogger(__name__)

# Ensure NUMBER platform is supported by modbus consts
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the DRP Modbus Boards integration from YAML.

    - Legge la sezione drp_modbus_boards_v2 dallo YAML
    - Crea/aggiorna le ConfigEntry per ogni hub definito
    - Rimuove le ConfigEntry che non sono più presenti nello YAML
    - Registra il servizio admin di reload (drp_modbus_boards_v2.reload)
    """
    hass.data.setdefault(DOMAIN, {})

    domain_cfg = config.get(DOMAIN)
    if not domain_cfg:
        log_warning(_LOGGER, "Domain '%s' not in ConfigType.", DOMAIN)
        return True

    # Lista di blocchi YAML per il dominio (uno per hub)
    # Esempio: [{'name': '...', 'type': 'tcp', 'host': '...', 'port': 502, 'devices': [...]}, ...]
    existing_entries = hass.config_entries.async_entries(DOMAIN)

    if existing_entries:
        # Entry esistenti indicizzate per name
        by_name = {e.data.get(CONF_NAME, DEFAULT_HUB): e for e in existing_entries}

        # Tracciamo i nomi presenti nel nuovo YAML
        yaml_names: set[str] = set()

        # Aggiorna entry esistenti / crea nuove entry
        for hub_cfg in domain_cfg:
            name = hub_cfg.get(CONF_NAME, DEFAULT_HUB)
            yaml_names.add(name)

            try:
                if name in by_name:
                    # Aggiorna l'entry esistente con il nuovo YAML
                    log_info(
                        _LOGGER,
                        "%s: aggiorno entry esistente '%s' con nuova config YAML.",
                        DOMAIN,
                        name,
                    )
                    hass.config_entries.async_update_entry(by_name[name], data=hub_cfg)
                else:
                    # Crea una nuova entry da YAML
                    log_info(
                        _LOGGER,
                        "%s: creo nuova entry da YAML per hub '%s'.",
                        DOMAIN,
                        name,
                    )
                    hass.async_create_task(
                        hass.config_entries.flow.async_init(
                            DOMAIN,
                            context={"source": SOURCE_IMPORT},
                            data=hub_cfg,
                        )
                    )
            except Exception as err:  # noqa: BLE001
                log_warning(
                    _LOGGER,
                    "%s: errore import/config update per hub '%s': %s",
                    DOMAIN,
                    name,
                    err,
                )

        # Rimuovi le entry che non sono più presenti nello YAML
        for entry in existing_entries:
            name = entry.data.get(CONF_NAME, DEFAULT_HUB)
            if name not in yaml_names:
                log_info(
                    _LOGGER,
                    "%s: rimuovo entry '%s' non più presente nello YAML.",
                    DOMAIN,
                    name,
                )
                await hass.config_entries.async_remove(entry.entry_id)

    else:
        # Prima inizializzazione: crea una entry per ogni hub in YAML
        for hub_cfg in domain_cfg:
            name = hub_cfg.get(CONF_NAME, DEFAULT_HUB)
            log_info(
                _LOGGER,
                "%s: prima inizializzazione, creo entry da YAML per hub '%s'.",
                DOMAIN,
                name,
            )
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": SOURCE_IMPORT},
                    data=hub_cfg,
                )
            )

    # Registra il servizio admin per ricaricare la config YAML on-demand
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_RELOAD,  # drp_modbus_boards_v2.reload
        lambda call: _reload_config(hass, call),
    )

    # Non chiamare async_modbus_setup qui: viene gestito in async_setup_entry
    log_info(_LOGGER, "%s: setup completed.", DOMAIN)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a DRP Modbus Board from a config entry.

    - ENTRY SOURCE_USER + yaml_only=True  -> placeholder creato da UI,
      nessun setup Modbus (configurazione gestita da YAML).
    - ENTRY SOURCE_IMPORT (da YAML)       -> setup completo hub Modbus.
    """

    # 1) Gestione entry placeholder creata da UI
    if (
        entry.source == config_entries.SOURCE_USER
        and entry.data.get("yaml_only") is True
    ):
        log_info(
            _LOGGER,
            "%s: UI placeholder entry '%s' (configurazione gestita da YAML). Nessun setup runtime.",
            DOMAIN,
            entry.title,
        )
        return True

    # 2) Setup reale per gli hub definiti in YAML (SOURCE_IMPORT)
    domain_store = hass.data.setdefault(DOMAIN, {})
    modbus_store = domain_store.setdefault(DATA_MODBUS_HUBS, {})

    # Config of the hub serialized in the entry (originates from YAML)
    yaml_for_this_hub: dict[str, Any] = dict(entry.data)

    # Optional: apply overrides from Options
    if entry.options:
        yaml_for_this_hub = {**yaml_for_this_hub, **entry.options}

    # Start core Modbus for this hub
    hacfg = build_modbus_ha_config(yaml_for_this_hub)
    wrapped: dict = {MODBUS_DOMAIN: hacfg}

    modbus_setup_result = await async_modbus_setup(hass, wrapped)
    if not modbus_setup_result:
        log_warning(
            _LOGGER,
            "%s: async_modbus_setup failed for '%s'",
            DOMAIN,
            entry.entry_id,
        )
        # Facciamo capire a HA che l'entry non è ancora pronta e va ritentata
        raise ConfigEntryNotReady("async_modbus_setup failed")

    # log_debug(
    #     _LOGGER,
    #     "xyz -------> %s",
    #     hass.data[DATA_MODBUS_HUBS],
    # )

    # Collect modbus hub in our integration store
    name = yaml_for_this_hub.get(CONF_NAME)
    connection_type = yaml_for_this_hub.get(CONF_TYPE)
    host = yaml_for_this_hub.get(CONF_HOST)
    port = yaml_for_this_hub.get(CONF_PORT)

    modbus_hub_key = slugify(f"{connection_type} {host} {port}")

    if modbus_hub_key not in modbus_store and name in hass.data[DATA_MODBUS_HUBS]:
        modbus_store[modbus_hub_key] = hass.data[DATA_MODBUS_HUBS].get(name)
    elif name not in hass.data[DATA_MODBUS_HUBS]:
        log_warning(
            _LOGGER,
            "%s: async_modbus_setup '%s' not in hass.data[DATA_MODBUS_HUBS]",
            DOMAIN,
            name,
        )

    # Create our coordinator using that dict
    gateway_name = yaml_for_this_hub.get(CONF_NAME, DEFAULT_HUB)
    coord = ModbusCoordinator(hass=hass, config_type=yaml_for_this_hub)

    # Prima refresh del coordinator: se fallisce, ConfigEntryNotReady e nessuna piattaforma viene creata
    await coord.async_config_entry_first_refresh()

    # Solo dopo una first_refresh riuscita, salviamo il coordinator e forwardiamo le piattaforme
    domain_store.setdefault(COORDINATORS, {})[gateway_name] = coord

    # Forward platform setups
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload when options change via UI
    entry.async_on_unload(entry.add_update_listener(_options_updated))

    log_info(
        _LOGGER,
        "%s: setup entry for entry id '%s' completed. Modbus gateway name '%s'",
        DOMAIN,
        entry.entry_id,
        gateway_name,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    # Cleanup coordinator/hub if needed
    if unload_ok:
        hub_name = entry.data.get(CONF_NAME, DEFAULT_HUB)
        domain_store = hass.data.get(DOMAIN, {})
        coord_store = domain_store.get(COORDINATORS, {})
        coord_store.pop(hub_name, None)

        # opzionale: ripulisci anche il modbus_store
        connection_type = entry.data.get(CONF_TYPE)
        host = entry.data.get(CONF_HOST)
        port = entry.data.get(CONF_PORT)
        modbus_hub_key = slugify(f"{connection_type} {host} {port}")
        modbus_store = domain_store.get(DATA_MODBUS_HUBS, {})
        modbus_store.pop(modbus_hub_key, None)

    return unload_ok


async def _options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload when Options change from UI."""
    _LOGGER.debug("%s: options aggiornate per %s → reload", DOMAIN, entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)


async def _reload_config(hass: HomeAssistant, call: Event | ServiceCall) -> None:
    """Ricarica la configurazione YAML e sincronizza le Config Entries.

    - Rilegge configuration.yaml (sezione drp_modbus_boards_v2)
    - Aggiorna le entry esistenti (per name) e le ricarica
    - Crea nuove entry per nuovi hub in YAML
    """
    log_info(
        _LOGGER,
        "%s: richiesta di reload configurazione YAML ricevuta.",
        DOMAIN,
    )

    reload_config: dict[str, Any] | None = await async_integration_yaml_config(hass, DOMAIN)

    if not reload_config or DOMAIN not in reload_config:
        log_warning(
            _LOGGER,
            "%s: Modbus domain non presente più nello YAML. Nessun hub da configurare.",
            DOMAIN,
        )
        return

    new_cfg: list[dict[str, Any]] = reload_config[DOMAIN]
    log_debug(
        _LOGGER,
        "%s: YAML riletto, trovati %d hub.",
        DOMAIN,
        len(new_cfg),
    )

    # Entry esistenti per questo dominio
    existing_entries = hass.config_entries.async_entries(DOMAIN)
    by_name = {e.data.get(CONF_NAME, DEFAULT_HUB): e for e in existing_entries}

    # Tracciamo i nomi presenti nel nuovo YAML
    yaml_names: set[str] = set()

    for hub_cfg in new_cfg:
        name = hub_cfg.get(CONF_NAME, DEFAULT_HUB)
        yaml_names.add(name)

        if name in by_name:
            entry = by_name[name]
            log_info(
                _LOGGER,
                "%s: aggiorno entry esistente '%s' con nuova config YAML.",
                DOMAIN,
                name,
            )
            # Aggiorna i dati dell'entry e ricaricala
            hass.config_entries.async_update_entry(entry, data=hub_cfg)
            await hass.config_entries.async_reload(entry.entry_id)
        else:
            log_info(
                _LOGGER,
                "%s: creo nuova entry da YAML per hub '%s'.",
                DOMAIN,
                name,
            )
            await hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data=hub_cfg,
            )

    # (Opzionale) rimuovere entry che NON sono più presenti nello YAML
    for entry in existing_entries:
        name = entry.data.get(CONF_NAME, DEFAULT_HUB)
        if name not in yaml_names:
            log_info(
                _LOGGER,
                "%s: rimuovo entry '%s' non più presente nello YAML.",
                DOMAIN,
                name,
            )
            await hass.config_entries.async_remove(entry.entry_id)

    log_info(_LOGGER, "%s: reload configurazione YAML completato.", DOMAIN)
