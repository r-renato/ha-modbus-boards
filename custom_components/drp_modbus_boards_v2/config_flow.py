from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_NAME

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow per DRP Modbus Boards.

    - Da UI (SOURCE_USER) crea una entry "placeholder" solo per mostrare
      l'integrazione e le sue dipendenze.
    - La configurazione reale degli hub Modbus resta gestita via YAML
      (SOURCE_IMPORT).
    """

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step iniziale da UI.

        Creiamo una entry "placeholder" per permettere di visualizzare
        l'integrazione e le sue dipendenze nella UI, ma la configurazione
        effettiva degli hub resta in YAML.
        """

        # Se esiste già una entry placeholder creata da UI, evitiamo duplicati
        for entry in self._async_current_entries():
            if (
                entry.source == config_entries.SOURCE_USER
                and entry.data.get("yaml_only") is True
            ):
                return self.async_abort(reason="already_configured")

        # Crea una entry minimale, marcata come "yaml_only"
        return self.async_create_entry(
            title="DRP Modbus (configurazione YAML)",
            data={"yaml_only": True},
        )

    async def async_step_import(
        self, import_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Creato da YAML: conserva lo YAML in entry.data e deduplica per name.

        Ogni hub definito in YAML genera (o aggiorna) una ConfigEntry con
        sorgente SOURCE_IMPORT e dati completi per quell'hub.
        """

        title = import_data.get(CONF_NAME) or "DRP Modbus"

        # Evita duplicati per lo stesso 'name' (solo tra entry di tipo IMPORT)
        for entry in self._async_current_entries():
            if entry.source != config_entries.SOURCE_IMPORT:
                continue

            if entry.data.get(CONF_NAME) == import_data.get(CONF_NAME):
                # Aggiorna l'entry esistente con il nuovo YAML
                self.hass.config_entries.async_update_entry(entry, data=import_data)
                return self.async_abort(reason="already_configured")

        # Crea una nuova entry per questo hub Modbus
        return self.async_create_entry(title=title, data=import_data)
