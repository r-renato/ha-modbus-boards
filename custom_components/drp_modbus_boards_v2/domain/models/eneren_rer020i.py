"""Registers mapping for Eneren RER 020 I board."""
from __future__ import annotations

from homeassistant.components.number import NumberMode
from homeassistant.const import Platform
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_REGISTER_INPUT,
    CALL_TYPE_COIL,
    CALL_TYPE_DISCRETE,
    CALL_TYPE_WRITE_COILS,
    CALL_TYPE_WRITE_REGISTERS,
    DataType,
)

from ...helpers.boards import register_board
from ...helpers.ha import ensure_number_in_platforms
from ...const import CONF_NUMBERS
from ..boards import BoardDefinition, Metadata, Register, RegisterArea, RegisterFunction, RegisterFunctionRead, RegisterFunctionWrite
from ..enums import Board, EnerenRER020IBinarySensorFunction, EnerenRER020INumberFunction, EnerenRER020ISensorFunction, EnerenRER020ISwitchFunction, RegisterAreaName

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   ENEREN RER 020 I
####### ####### ####### ####### #######

@register_board(Board.ENEREN_RER020I_EFHR0_EVO)
def _eneren_rer020i_regs() -> BoardDefinition:
    return BoardDefinition(
        metadata = Metadata(name="Dehumidifier with fresh-air renewal (VMC)", manufacturer="eneren", model="rer_020i"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x00,
                count=26,
                
                mdb_read_function=CALL_TYPE_DISCRETE,
                data_type=DataType.UINT16,

            ),
            RegisterAreaName.AREA_B: RegisterArea(
                address=0x00,
                count=28,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.UINT16,
            ),
            RegisterAreaName.AREA_C: RegisterArea(
                address=0x00,
                count=24,
                
                mdb_read_function=CALL_TYPE_COIL,
                mdb_write_function=CALL_TYPE_WRITE_COILS,

                data_type=DataType.UINT16,

                state_on=True,  # relay state close (on)
                state_off=False, # relay state open (off)

                command_on=0x01,   # Relay command close
                command_off=0x00,  # Relay command open
            ),
            RegisterAreaName.AREA_D: RegisterArea(
                address=0x00,
                count=21,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTERS,
                data_type=DataType.UINT16,
            ),
        },
        registers={
            Platform.BINARY_SENSOR: Register(
                functions={
                    EnerenRER020IBinarySensorFunction.PRESENZA_ALLARME: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x00,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_AVVERTIMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x01,
                    ),
                    EnerenRER020IBinarySensorFunction.FILTRI_DA_PULIRE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x02,
                    ),
                    EnerenRER020IBinarySensorFunction.MANCANZA_COMUNICAZIONE_CON_DISPLAY: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x03,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_OPZIONE_SERRANDE_ESTERNE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x07,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_OPZIONE_SBRINAMENTO_RECUPERATORE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x08,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_FREE_COOLING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x09,
                    ),
                    EnerenRER020IBinarySensorFunction.ALLARME_SONDA: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0A,
                    ),
                    EnerenRER020IBinarySensorFunction.ALLARME_SONDA_CO2_AMBIENTE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0B,
                    ),
                    EnerenRER020IBinarySensorFunction.ALLARME_ALTA_PRESSIONE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0C,
                    ),
                    EnerenRER020IBinarySensorFunction.AVVERTIMENTO_BASSA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0D,
                    ),
                    EnerenRER020IBinarySensorFunction.AVVERTIMENTO_ALTA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0E,
                    ),
                    EnerenRER020IBinarySensorFunction.AVVERTIMENTO_RISCHIO_CONGELAMENTO_BATTERIA_ACQUA: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0F,
                    ),
                    EnerenRER020IBinarySensorFunction.ALLARME_DEW_POINT: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x10,
                    ),
                    EnerenRER020IBinarySensorFunction.STATO_COMPRESSORE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x11,
                    ),
                    EnerenRER020IBinarySensorFunction.STATO_FREE_COOLING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x12,
                    ),
                    EnerenRER020IBinarySensorFunction.RICHIESTA_ACQUA_DA_IMPIANTO: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x13,
                    ),
                    EnerenRER020IBinarySensorFunction.RICHIESTA_DEUMIDIFICA: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x14,
                    ),
                    EnerenRER020IBinarySensorFunction.RICHIESTA_RAFFREDDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x15,
                    ),
                    EnerenRER020IBinarySensorFunction.RICHIESTA_RISCALDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x16,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_SONDA_T_MANDATA_ARIA: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x17,
                    ),
                    EnerenRER020IBinarySensorFunction.CONTROLLO_TEMPERATURA_MANDATA_ONOFF_ATTIVO: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x18,
                    ),
                    EnerenRER020IBinarySensorFunction.PRESENZA_FUNZIONE_CONTROLLO_TEMPERATURA_DI_MANDATA_MODULANTE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x19,
                    ),
                },
            ),

            Platform.SENSOR: Register(
                functions={
                    EnerenRER020ISensorFunction.TEMPERATURA_AMBIENTE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x00,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),
                    EnerenRER020ISensorFunction.UMIDITA_RELATIVA_AMBIENTE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x01,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="humidity",
                        unit_of_measurement="%",
                    ),
                    EnerenRER020ISensorFunction.SONDA_CO2: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x02,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="co2",
                        unit_of_measurement="ppm",
                    ),
                    EnerenRER020ISensorFunction.TEMPERATURA_ACQUA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x10,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),
                    EnerenRER020ISensorFunction.TEMPERATURA_ESTERNA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x11,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),
                    EnerenRER020ISensorFunction.STATO_VENTILATORE_MANDATA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x12,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class=None,
                        unit_of_measurement="%",
                    ),
                    EnerenRER020ISensorFunction.STATO_VENTILATORE_ESTRAZIONE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x13,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class=None,
                        unit_of_measurement="%",
                    ),
                    EnerenRER020ISensorFunction.SET_TEMPERATURE_EFFETTIVO: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x14,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),
                    EnerenRER020ISensorFunction.SET_UMIDITA_EFFETTIVO: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x15,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="humidity",
                        unit_of_measurement="%",
                    ),
                    EnerenRER020ISensorFunction.SET_RICAMBIO_EFFETTIVO: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x16,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                    ),
                    EnerenRER020ISensorFunction.ORE_FUNZIONAMENTO_UNITA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x17,
                        state_class="measurement",

                    ),
                    EnerenRER020ISensorFunction.RELEASE_SOFTWARE_SCHEDA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x18,
                    ),
                    EnerenRER020ISensorFunction.TEMPERATURA_MANDATA_ARIA: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x19,
                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),
                },
            ),

            Platform.SWITCH: Register(
                functions={
                    EnerenRER020ISwitchFunction.DEVICE_POWER_CONTROL: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x00,
                    ),
                    EnerenRER020ISwitchFunction.STAGIONE: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x01,

                        description="0=Summer, 1=Winter"
                    ),
                    EnerenRER020ISwitchFunction.FORZATURA_OFF_TRATTAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x02,
                    ),
                    EnerenRER020ISwitchFunction.RESET_ALLARMI: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x03,
                    ),
                    EnerenRER020ISwitchFunction.RESET_PULIZIA_FILTRI: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x04,
                    ),
                    EnerenRER020ISwitchFunction.ABILITAZIONE_FORZATURA_FREE_COOLING: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x08,
                    ),
                    EnerenRER020ISwitchFunction.FORZATURA_FREE_COOLING: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x09,
                    ),
                    EnerenRER020ISwitchFunction.FORZATURA_RISCALDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x0C,
                    ),
                    EnerenRER020ISwitchFunction.FORZATURA_RAFFREDDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x0D,
                    ),
                    EnerenRER020ISwitchFunction.ABILITAZIONE_FORZATURA_DEUMIDIFICA_UMIDIFICA: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x0E,
                    ),
                    EnerenRER020ISwitchFunction.FORZATURA_DEUMIDIFICA: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x0F,
                    ),
                    EnerenRER020ISwitchFunction.RICHIESTA_VENTILAZIONE_DI_RICIRCOLO: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x10,

                        description="Solo se non sono attive richieste di trattamento o altre funzioni di protezione"
                    ),
                    EnerenRER020ISwitchFunction.UNITA_MISURA_TEMPERATURA: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x11,

                        description= "0=Celsius, 1=Fahrenheit"
                    ),
                    EnerenRER020ISwitchFunction.GESTIONE_CONTROLLO_TEMPERATURA_MANDATA: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x15,

                        description="0=Utilizzo della sonda di temperatura mandata (se presente opzione controllo di temperatura di mandata modulante), "
                        "1=Utilizzo della sonda di temperatura ambiente"
                    ),
                    EnerenRER020ISwitchFunction.GESTIONE_CONTROLLO_DEW_POINT: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x16,

                        description="0. Dew-point variabile (T superficiale = T acqua + differenziale. "
                        "La T acqua viene misurata dalla macchina; differenziale e T dew-point sono parametri impostabili), "
                        "1=Dew-point fisso (T superficiale)"
                    ),
                },
            ),

            Platform.NUMBER: Register(
                functions={
                    EnerenRER020INumberFunction.SET_TEMPERATURE_AMBIENTE_IN_CENSIUS: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x00,

                        min=15,
                        max=30,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=0.1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),

                    EnerenRER020INumberFunction.SET_UMIDITA_RELATIVA_AMBIENTE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x01,

                        min=40,
                        max=90,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=0.1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="humidity",
                        unit_of_measurement="%",
                    ),

                    EnerenRER020INumberFunction.SET_RICAMBIO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x02,

                        min=0,
                        max=5,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_ORE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x03,

                        min=0,
                        max=23,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_MINUTI: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x04,

                        min=0,
                        max=59,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_GIORNO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x05,

                        default=0,
                        min=0,
                        max=31,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,

                        description="0 (zero) disabled"
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_MESE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x06,

                        default=0,
                        min=1,
                        max=12,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,

                        description="0 (zero) disabled"
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_ANNO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x07,

                        default=0,
                        min=10,
                        max=99,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,

                        description="0 (zero) disabled"
                    ),

                    EnerenRER020INumberFunction.OROLOGIO_GIORNO_DELLA_SETTIMANA: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x08,

                        min=0,
                        max=6,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,
                    ),

                    EnerenRER020INumberFunction.FORZATURA_VALVOLA_ACQUA_MODULANTE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0A,

                        min=0,
                        max=100,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement="%",
                    ),

                    EnerenRER020INumberFunction.TEMPERATURA_MINIMA_INVERNALE_SENZA_RISCALDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0B,

                        min=0,
                        max=90,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),

                    EnerenRER020INumberFunction.TEMPERATURA_MASSIMA_ESTIVA_SENZA_RAFFREDDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0C,

                        min=0,
                        max=90,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),

                    EnerenRER020INumberFunction.GESTIONE_RAFFREDDAMENTO: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0D,

                        min=0,
                        max=2,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,

                        description="0=Utilizzo del solo compressore, "
                                    "1=Utilizzo solo dell'acqua, "
                                    "2=Prima l'acqua, se non sufficiente compressore",
                    ),

                    EnerenRER020INumberFunction.PROTEZIONE_DEW_POINT_DIFFERENZIALE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0E,

                        min=-10,
                        max=10,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),

                    EnerenRER020INumberFunction.PROTEZIONE_DEW_POINT_VALORE_T_DEW_POINT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0F,

                        min=10,
                        max=40,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=0.1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                    ),

                    EnerenRER020INumberFunction.ORE_ATTESA_PROMEMORIA_PULIZIA_FILTRI_SPORCHI: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x10,

                        min=720,
                        max=4320,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=0.1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,
                    ),

                    EnerenRER020INumberFunction.RICHIESTA_ATTIVAZIONE_COMPRESSORE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x13,

                        min=0,
                        max=2,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            step=1,
                            number_mode=NumberMode.BOX,
                        ),

                        state_class=None,
                        device_class=None,
                        unit_of_measurement=None,

                        description="0=Deumidifica o raffreddamento, "
                                    "1=Solo deumidifica, "
                                    "2=Solo raffreddamento",
                    ),
                },
            ),



        },
    ) 



