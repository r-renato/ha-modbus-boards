#
from enum import Enum, IntEnum, StrEnum

from homeassistant.const import (
    CONF_BINARY_SENSORS,
    CONF_COVERS,
    CONF_LIGHTS,
    CONF_SENSORS,
    CONF_SWITCHES,
    Platform,
)
from .const import (
    CONF_CLIMATES,
    CONF_FANS,
    CALL_TYPE_COIL,
    CALL_TYPE_DISCRETE,
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_REGISTER_INPUT,
    CALL_TYPE_WRITE_COIL,
    CALL_TYPE_WRITE_COILS,
    CALL_TYPE_WRITE_REGISTER,
    CALL_TYPE_WRITE_REGISTERS,
    CALL_TYPE_X_COILS,
    CALL_TYPE_X_REGISTER_HOLDINGS,
    DataType,
)

CONF_BOARD_DEVICE = "device"
CONF_BOARD = "board"
CONF_NUMBERS = "numbers"
CONF_REVERSE = "reverse"
CONF_SWITCH_CONSTRAINT = "switch_constraint"

MODBUS_DOMAIN = "drp_modbus_boards"
DEFAULT_NAME = "drp_modbus_boards"
DEFAULT_HUB = "drp_modbus_boards_hub"
DEFAULT_MODBUS_ADDRESS = 1
DEFAULT_SCAN_INTERVAL = 60  # seconds

STRUCTUREMAP = {
    DataType.INT8 : ">b",
    DataType.INT16 : ">h",
    DataType.INT32 : ">i",
    DataType.INT64 : ">q",
    DataType.UINT8 : ">B",
    DataType.UINT16 : ">H",
    DataType.UINT32 : ">I",
    DataType.UINT64 : ">Q",
    DataType.FLOAT16 : ">e",
    DataType.FLOAT32 : ">f",
    DataType.FLOAT64 : ">d",
}

PLATFORMS = (
    (Platform.BINARY_SENSOR, CONF_BINARY_SENSORS),
    (Platform.CLIMATE, CONF_CLIMATES),
    (Platform.COVER, CONF_COVERS),
    (Platform.LIGHT, CONF_LIGHTS),
    (Platform.FAN, CONF_FANS),
    (Platform.SENSOR, CONF_SENSORS),
    (Platform.SWITCH, CONF_SWITCHES),
    (Platform.NUMBER, CONF_NUMBERS),
)

MODE_SLIDER = "slider"
MODE_BOX = "box"

METADATA = "metadata"

RN_TEMPERATURE = "temperature"
RN_HUMIDITY = "humidity"

RN_CHANNEL_00 = "channel_00"
RN_CHANNEL_01 = "channel_01"
RN_CHANNEL_02 = "channel_02"
RN_CHANNEL_03 = "channel_03"
RN_CHANNEL_04 = "channel_04"
RN_CHANNEL_05 = "channel_05"
RN_CHANNEL_06 = "channel_06"
RN_CHANNEL_07 = "channel_07"
RN_CHANNEL_08 = "channel_08"
RN_CHANNEL_09 = "channel_09"
RN_CHANNEL_10 = "channel_10"
RN_CHANNEL_11 = "channel_11"
RN_CHANNEL_12 = "channel_12"
RN_CHANNEL_13 = "channel_13"
RN_CHANNEL_14 = "channel_14"
RN_CHANNEL_15 = "channel_15"

RN_VIN2_VALUE = "vin2_value"
RN_VIN2_VALUE_PERCENTAGE = "vin2_value_percentage"
RN_VOUT2_VALUE = "vout2_value"
RN_VOUT2_VALUE_PERCENTAGE = "vout2_value_percentage"

RN_VOLTAGE = "ro_voltage"
RN_CURRENT = "ro_current"
RN_ACTIVE_POWER = "ro_active_power"
RN_TOTAL_ACTIVE_ENERGY = "ro_total_active_energy"

####### ####### ####### ####### #######
#   RER
####### ####### ####### ####### #######

RER_PRESENZA_ALLARME = "ro_presenza_allarme"
RER_PRESENZA_AVVERTIMENTO = "ro_presenza_avvertimento"
RER_FILTRI_DA_PULIRE = "ro_filtri_da_pulire"
RER_MANCANZA_COMUNICAZIONE_CON_DISPLAY = "ro_mancanza_comunicazione_con_display"
RER_PRESENZA_OPZIONE_SERRANDE_ESTERNE = "ro_presenza_opzione_serrande_esterne"
RER_PRESENZA_OPZIONE_SBRINAMENTO_RECUPERATORE = "ro_presenza_opzione_sbrinamento_recuperatore"
RER_PRESENZA_FREE_COOLING = "ro_presenza_free_cooling"
RER_ALLARME_SONDA = "ro_allarme_sonda"
RER_ALLARME_SONDA_CO2_AMBIENTE = "ro_allarme_sonda_co2_ambiente"
RER_ALLARME_ALTA_PRESSIONE = "ro_allarme_alta_pressione"
RER_AVVERTIMENTO_BASSA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE = "ro_avvertimento_bassa_temperatura_acqua_per_on_compressore"
RER_AVVERTIMENTO_ALTA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE = "ro_avvertimento_alta_temperatura_acqua_per_on_compressore"
RER_AVVERTIMENTO_RISCHIO_CONGELAMENTO_BATTERIA_ACQUA = "ro_avvertimento_rischio_congelamento_batteria_acqua"
RER_ALLARME_DEW_POINT = "ro_allarme_dew_point"
RER_STATO_COMPRESSORE = "ro_stato_compressore"
RER_STATO_FREE_COOLING = "ro_stato_free_cooling"
RER_RICHIESTA_ACQUA_DA_IMPIANTO = "ro_richiesta_acqua_da_impianto"
RER_RICHIESTA_DEUMIDIFICA = "ro_richiesta_deumidifica"
RER_RICHIESTA_RAFFREDDAMENTO = "ro_richiesta_raffreddamento"
RER_RICHIESTA_RISCALDAMENTO = "ro_richiesta_riscaldamento"
RER_PRESENZA_SONDA_T_MANDATA_ARIA = "ro_presenza_sonda_t_mandata_aria"
RER_CONTROLLO_TEMPERATURA_MANDATA_ONOFF_ATTIVO = "ro_controllo_temperatura_di_mandata_onoff_attivo"
RER_PRESENZA_FUNZIONE_CONTROLLO_TEMPERATURA_DI_MANDATA_MODULANTE = "ro_presenza_funzione_controllo_di_temperatura_di_mandata_modulante"

RER_DEVICE_POWER_CONTROL = "rw_device_power_control"
RER_STAGIONE = "rw_stagione"
RER_FORZATURA_OFF_TRATTAMENTO = "rw_forzatura_off_trattamento"
RER_RESET_ALLARMI= "rw_reset_allarmi"
RER_RESET_PULIZIA_FILTRI = "rw_reset_pulizia_filtri"
RER_ABILITAZIONE_FORZATURA_FREE_COOLING = "rw_abilitazione_forzatura_free_cooling"
RER_FORZATURA_FREE_COOLING = "rw_forzatura_free_cooling"
RER_FORZATURA_RISCALDAMENTO = "rw_forzatura_riscaldamento"
RER_FORZATURA_RAFFREDDAMENTO = "rw_forzatura_raffreddamento"
RER_ABILITAZIONE_FORZATURA_DEUMIDIFICA_UMIDIFICA = "rw_abilitazione_forzatura_deumidifica_umidifica"
RER_FORZATURA_DEUMIDIFICA = "rw_forzatura_deumidifica"
RER_RICHIESTA_VENTILAZIONE_DI_RICIRCOLO = "rw_richiesta_ventilazione_di_ricircolo"
RER_UNITA_MISURA_TEMPERATURA = "rw_unita_di_misura_temperatura"
RER_GESTIONE_CONTROLLO_TEMPERATURA_MANDATA = "rw_gestione_controllo_temperatura_mandata"
RER_GESTIONE_CONTROLLO_DEW_POINT = "rw_gestione_controllo_dew_point"

RER_SET_TEMPERATURE_AMBIENTE_IN_CENSIUS = "rw_set_temperatura_ambiente_in_celsius"
RER_SET_UMIDITA_RELATIVA_AMBIENTE = "rw_set_umidita_relativa_ambiente"
RER_SET_RICAMBIO = "rw_set_ricambio"
RER_OROLOGIO_ORE = "rw_orologio_ore"
RER_OROLOGIO_MINUTI = "rw_orologio_minuti"
RER_OROLOGIO_GIORNO = "rw_orologio_giorno"
RER_OROLOGIO_MESE = "rw_orologio_mese"
RER_OROLOGIO_ANNO = "rw_orologio_anno"
RER_OROLOGIO_GIORNO_DELLA_SETTIMANA = "rw_orologio_giorno_della_settimana"
RER_FORZATURA_VALVOLA_ACQUA_MODULANTE = "rw_forzatura_valvola_acqua_modulante"
RER_TEMPERATURA_MINIMA_INVERNALE_SENZA_RISCALDAMENTO = "rw_temperatura_minima_invernale_senza_riscaldamento"
RER_TEMPERATURA_MASSIMA_ESTIVA_SENZA_RAFFREDDAMENTO = "rw_temperatura_massima_estiva_senza_raffreddamento"
RER_GESTIONE_RAFFREDDAMENTO = "rw_gestione_raffreddamento"
RER_PROTEZIONE_DEW_POINT_DIFFERENZIALE = "rw_protezione_dew_point_differenziale"
RER_PROTEZIONE_DEW_POINT_VALORE_T_DEW_POINT = "rw_protezione_dew_point_valore_t_dew_point"
RER_ORE_ATTESA_PROMEMORIA_PULIZIA_FILTRI_SPORCHI = "rw_ore_di_attesa_promemoria_pulizia_filtri_sporchi"
RER_RICHIESTA_ATTIVAZIONE_COMPRESSORE = "rw_richiesta_attivazione_compressore"

RER_TEMPERATURA_AMBIENTE = "ro_temperatura_ambiente"
RER_UMIDITA_RELATIVA_AMBIENTE = "ro_umidita_relativa_ambiente"
RER_SONDA_CO2 = "ro_sonda_co2"
RER_TEMPERATURA_ACQUA = "ro_temperatura_acqua"
RER_TEMPERATURA_ESTERNA = "ro_temperatura_esterna"
RER_STATO_VENTILATORE_MANDATA = "ro_stato_ventilatore_mandata"
RER_STATO_VENTILATORE_ESTRAZIONE = "ro_stato_ventilatore_estrazione"
RER_SET_TEMPERATURE_EFFETTIVO = "ro_set_temperatura_effettivo"
RER_SET_UMIDITA_EFFETTIVO = "ro_set_umidita_effettivo"
RER_SET_RICAMBIO_EFFETTIVO = "ro_set_ricambio_effettivo"
RER_ORE_FUNZIONAMENTO_UNITA = "ro_ore_funzionamento_unita"
RER_RELEASE_SOFTWARE_SCHEDA = "ro_release_software_scheda"
RER_TEMPERATURA_MANDATA_ARIA = "ro_temperatura_mandata_aria"

HMI080_DEVICE_POWER_CONTROL = "rw_device_power_control"

HMI080_RW_WEEKLY_TIMER = "rw_weekly_timer"
HMI080_RW_CLOCK_TIMER = "rw_clock_timer"
HMI080_RW_TEMP_TIMER = "rw_temp_timer"
HMI080_RW_GATE_CTRL = "rw_gate_ctrl"
HMI080_RW_SOLAR_HEATER = "rw_solar_heater"
HMI080_RW_CTRL_STATE = "rw_ctrl_state"
HMI080_RW_FAST_HOT_WATER = "rw_fast_hot_water"
HMI080_RW_COOL_AND_HOT_WATER_PRIORITY = "rw_cool_and_hot_water_priority"
HMI080_RW_HEAT_AND_HOT_WATER_PRIORITY = "rw_heat_and_hot_water_priority"
HMI080_RW_QUITE_MODE = "rw_quite_mode"
HMI080_RW_WEATHER_DEPEND = "rw_weather_depend"
HMI080_RW_DISINFECTION = "rw_disinfection"
HMI080_RW_FLOOR_DEBUG = "rw_floor_debug"
HMI080_RW_FLOOR_DEBUG_START_STOP = "rw_floor_debug_start_stop"
HMI080_RW_EMERGENCE_MODE = "rw_emergence_mode"
HMI080_RW_OTHER_THERMAL = "rw_other_thermal"
HMI080_RW_WATER_TANK = "rw_water_tank"
HMI080_RW_SOLAR_SETTING = "rw_solar_setting"
HMI080_RW_REMOTE_SENSOR = "rw_remote_sensor"
HMI080_RW_HOLIDAY_MODE = "rw_holiday_mode"
HMI080_RW_REFRI_RECOVERY = "rw_refri_recovery"
HMI080_RW_MANUAL_DEFROST = "rw_manual_defrost"
HMI080_RW_COOL_2_WAY_VALVE = "rw_cool_2_way_valve"


HMI080_MODE = "rw_mode"
HMI080_OPTIONAL_E_HEATER = "rw_optional_e_heater"
HMI080_DISINFECTION_TEMP = "rw_disinfection_temp"
HMI080_FLOR_DEBUG_SEGMENTS = "rw_floor_debug_segments"
HMI080_FLOR_DEBUG_PERIOD_1_TEMP = "rw_floor_debug_period_1_temp"
HMI080_DELTA_T_OF_SEGMENT = "rw_delta_t_of_segment"
HMI080_SEGMENT_TIME = "rw_segment_time"
HMI080_WOT_COOL = "rw_wot_cool"
HMI080_WOT_HEAT = "rw_wot_heat"
HMI080_RT_COOL = "rw_rt_cool"
HMI080_RT_HEAT = "rw_rt_heat"
HMI080_T_WATER_TANK = "rw_t_water_tank"
HMI080_T_EHEATER = "rw_t_eheater"
HMI080_T_OTHER_SWITCH_ON = "rw_t_other_switch_on"
HMI080_T_HP_MAX = "rw_t_hp_max"
HMI080_UPPER_AT_HEAT = "rw_upper_at_heat"
HMI080_LOWER_AT_HEAT = "rw_lower_at_heat"
HMI080_UPPER_RT_HEAT = "rw_upper_rt_heat"
HMI080_LOWER_RT_HEAT = "rw_lower_rt_heat"
HMI080_UPPER_WT_HEAT = "rw_upper_wt_heat"
HMI080_LOWER_WT_HEAT = "rw_lower_wt_heat"
HMI080_UPPER_AT_COOL = "rw_upper_at_cool"
HMI080_LOWER_AT_COOL = "rw_lower_at_cool"
HMI080_UPPER_RT_COOL = "rw_upper_rt_cool"
HMI080_LOWER_RT_COOL = "rw_lower_rt_cool"
HMI080_UPPER_WT_COOL = "rw_upper_wt_cool"
HMI080_LOWER_WT_COOL = "rw_lower_wt_cool"
HMI080_DELTA_T_COOL = "rw_delta_t_cool"
HMI080_DELTA_T_HEAT = "rw_delta_t_heat"
HMI080_DELTA_T_HOT_WATER = "rw_delta_t_hot_water"
HMI080_DELTA_T_ROOM_TEMP = "rw_delta_t_room_temp"
HMI080_COOL_RUN_TIME = "rw_cool_run_time"
HMI080_HEAT_RUN_TIME = "rw_heat_run_time"
HMI080_OTHER_THERMAL_LOGIC = "rw_other_thermal_logic"
HMI080_TANK_HEATER = "rw_tank_heater"
HMI080_OPTIONAL_E_HEATER_LOGIC = "rw_optional_e_heater_logic"
HMI080_CURRENT_LIMIT_VALUE = "rw_current_limit_value"
HMI080_RW_THERMOSTAT = "rw_thermostat"
HMI080_FORCE_MODE = "rw_force_mode"
HMI080_AIR_REMOVAL = "rw_air_removal"

HMI080_UNIT_STATUS = "ro_unit_status"
HMI080_T_OUTDOOR = "ro_t_outdoor"
HMI080_T_DISCHARGE = "ro_t_discharge"
HMI080_T_DEFROST = "ro_t_defrost"
HMI080_T_SUCTION = "ro_t_suction"
HMI080_T_ECONOMIZER_IN = "ro_t_economizer_in"
HMI080_T_ECONOMIZER_OUT = "ro_t_economizer_out"
HMI080_DIS_PRESSURE = "ro_dis_pressure"
HMI080_T_WATER_OUT_PE = "ro_t_water_out_pe"
HMI080_T_OPTIONAL_WATER_SENS = "ro_t_optional_water_sen"
HMI080_T_WATER_IN_PE = "ro_t_water_in_pe"
HMI080_T_TANK_CTRL = "ro_t_tank_ctrl"
HMI080_T_REMOTE_ROOM = "ro_t_remote_room"
HMI080_T_GAS_PIPE = "ro_t_gas_pipe"
HMI080_T_LIQUID_PIPE = "ro_t_liquid_pipe"
HMI080_THERMOSTAT = "ro_thermostat"
HMI080_T_FLOOR_DEBUG = "ro_t_floor_debug"
HMI080_DEBUG_TIME = "ro_debug_time"
HMI080_DISINFECTION = "ro_disinfection"
HMI080_ERROR_TIME_FOR_FLOOR_DEBUG = "ro_error_time_for_floor_debug"
HMI080_T_WEATHER_DEPEND = "ro_t_weather_depend"

HMI080_HEAT_2_WAY_VALVE = "ro_heat_2_way_valve"
HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_IDU = "ro_communication_error_between_the_wired_controller_and_idu"
HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_ODU = "ro_communication_error_between_the_wired_controller_and_odu"
HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_DRIVE = "ro_communication_error_between_the_wired_controller_and_drive"
HMI080_HP_ANTIFREE = "ro_hp_antifree"
HMI080_COMPRESSOR_STATE = "ro_compressor_state"
HMI080_ODU_FAN_STATE = "ro_odu_fan_state"
HMI080_4_WAY_VALVE_STATE = "ro_4_way_valve_state"
HMI080_COMPRESSOR_CRANKCASE_HEATER_STATE = "ro_compressor_crankcase_heater_state"
HMI080_UNDERPAN_HEATER_STATE = "ro_underpan_heater_state"
HMI080_DEFROSTING_STATE = "ro_defrosting_state"
HMI080_OIL_RETURN_STATE = "ro_oil_return_state"
HMI080_AMBIENT_TEMP_SENSOR_ERROR = "ro_ambient_temp_sensor_error"
HMI080_DEFROST_TEMP_SENSOR_ERROR = "ro_defrost_temp_sensor_error"
HMI080_DISCHARGE_TEMP_SENSOR_ERROR = "ro_discharge_temp_sensor_error"
HMI080_SUCTION_TEMP_SENSOR_ERROR = "ro_suction_temp_sensor_error"
HMI080_ODU_FAN_ERROR = "ro_odu_fan_error"
HMI080_HIGH_PRESSURE_SENSOR_ERROR = "ro_high_pressure_sensor_error"
HMI080_HIGH_PRESSURE_PROTECTION = "ro_high_pressure_protection"
HMI080_LOW_PRESSURE_PROTECTION = "ro_low_pressure_protection"
HMI080_HIGH_DISCHARGE_PROTECTION = "ro_high_discharge_protection"
HMI080_CAPACITY_DIP_SETTING_ERROR = "ro_capacity_dip_setting_error"
HMI080_COMMUNICATION_ERROR_BETWEEN_IDU_AND_ODU = "ro_communication_error_between_idu_and_odu"
HMI080_ECONOMIZER_IN_SENSOR_ERROR = "ro_economizer_in_sensor_error"
HMI080_ECONOMIZER_OUT_SENSOR_ERROR = "ro_economizer_out_sensor_error"
HMI080_SYSTEM_RECOVERABLE_PROTECTION = "ro_system_recoverable_protection"
HMI080_SYSTEM_IRRECOVERABLE_PROTECTION = "ro_system_irrecoverable_protection"
HMI080_FLOW_SWITCH_PROTECTION = "ro_flow_switch_protection"
HMI080_DC_BUS_LOW_VOLTAGE_OR_VOLTAGE_DROP = "ro_dc_bus_low_voltage_or_voltage_drop"
HMI080_DC_BUS_OVER_VOLTAGE = "ro_dc_bus_over_voltage"
HMI080_AC_CURRENT_PROTECTION_INPUT_SIDE = "ro_ac_current_protection_input_side"
HMI080_IPM_ERROR = "ro_ipm_error"
HMI080_PFC_ERROR = "ro_pfc_error"
HMI080_STARTUP_ERROR = "ro_startup_error"
HMI080_PHASE_LOSS = "ro_phase_loss"
HMI080_DRIVE_MODULE_RESETTING = "ro_drive_module_resetting"
HMI080_COMPRESSOR_OVERCURRENT = "ro_compressor_overcurrent"
HMI080_OVER_SPEED = "ro_over_speed"
HMI080_CHARGING_CIRCUIT_ERROR_OR_CURRENT_SENSOR_ERROR = "ro_charging_circuit_error_or_current_sensor_error"
HMI080_DESYNCHRONIZING = "ro_desynchronizing"
HMI080_COMPRESSOR_STALLING = "ro_compressor_stalling"
HMI080_DRIVE_COMMUNICATION_ERROR = "ro_drive_communication_error"
HMI080_RADIATOR_OR_IPM_OR_PFC_OVER_TEMPERATURE = "ro_radiator_or_ipm_or_pfc_over_temperature"
HMI080_DEFECTIVE_RADIATOR_OR_IPM_OR_PFC = "ro_defective_radiator_or_ipm_or_pfc"
HMI080_CHARGING_CIRCUIT_ERROR = "ro_charging_circuit_error"
HMI080_AC_INPUT_VOLTAGE_ERROR = "ro_ac_input_voltage_error"
HMI080_DRIVE_BOARD_TEMP_SENSOR_ERROR = "ro_drive_board_temp_sensor_error"
HMI080_AC_CONTACTOR_PROTECTION_OR_INPUT_CROSS_ZERO_ERROR = "ro_ac_contactor_protection_or_input_cross_zero_error"
HMI080_TEMP_DRIFT_PROTECTION = "ro_temp_drift_protection"
HMI080_SENSOR_CONNECTION_PROTECTION_CONNN= "ro_sensor_connection_protection_connection_to_phase_u_or_v_failed"
HMI080_CONDENSER_LEAVING_WATER_TEMP_SENSOR_ERROR = "ro_condenser_leaving_water_temp_sensor_error"
HMI080_E_HEATER_LEAVING_WATER_TEMP_SENSOR_ERROR = "ro_e_heater_leaving_water_temp_sensor_error"
HMI080_REFRIGERANT_LIQUID_TEMP_SENSOR_ERROR = "ro_refrigerant_liquid_temp_sensor_error"
HMI080_CONDENSER_ENTERING_WATER_TEMP_SENSOR_ERROR = "ro_condenser_entering_water_temp_sensor_error"
HMI080_WATER_TANK_TEMP_SENSOR_ERROR = "ro_water_tank_temp_sensor_error"
HMI080_REFRIGERANT_VAPOR_LINE_TEMP_SENSOR_ERROR = "ro_refrigerant_vapor_line_temp_sensor_error"
HMI080_REMOTE_ROOM_TEMP_SENSOR_ERROR = "ro_remote_room_temp_sensor_error"
HMI080_OTHER_HEAT_SOURCE_STATE = "ro_other_heat_source_state"
HMI080_FLOW_SWITCH_STATE = "ro_flow_switch_state"
HMI080_IDU_E_HEATER_1_STATE = "ro_idu_e_heater_1_state"
HMI080_IDU_E_HEATER_2_STATE = "ro_idu_e_heater_2_state"
HMI080_WATER_TANK_HEATER_STATE = "ro_water_tank_heater_state"
HMI080_IDU_WATER_PUMP_STATE = "ro_idu_water_pump_state"
HMI080_CIRCULATING_2_WAY_VALVE_STATE = "ro_circulating_2_way_valve_state"
HMI080_PLATE_HEATER_STATE = "ro_plate_heater_state"
HMI080_3_WAY_VALVE_STATE = "ro_3_way_valve_state"
HMI080_GATE_CTRL = "ro_gate_ctrl"
HMI080_JUMPER_CAP_ERROR = "ro_jumper_cap_error"
HMI080_E_HEATER_1_WELDING_PROTECTION = "ro_e_heater_1_welding_protection"
HMI080_E_HEATER_2_WELDING_PROTECTION = "ro_e_heater_2_welding_protection"
HMI080_WATER_HEATER_WELDING_PROTECTION = "ro_water_heater_welding_protection"
HMI080_WATER_FLOW_PROTECTION = "ro_water_flow_protection"
HMI080_IDU_RECOVERABLE_PROTECTION = "ro_idu_recoverable_protection"
HMI080_IDU_IRRECOVERABLE_PROTECTION = "ro_idu_irrecoverable_protection"

class BoardBlock(StrEnum):
    REGISTERS_BLOCK_1 = "registers_block_1"
    REGISTERS_BLOCK_2 = "registers_block_2"

class Board(StrEnum):
    """Available Boards."""
    XY_MOD01_SHT20 = "xy_mod01_sht20"
    GL_TH02_PE = "gl_th02_pe",
    EASTRON_SDM120M = "eastron_sdm120m"
    ELETECHSUP_NT18B07 = "eletechsup_nt18b07"
    ELETECHSUP_N4DBA06 = "eletechsup_n4dba06"
    ELETECHSUP_R4D3B16 = "eletechsup_r4d3b16"
    ELETECHSUP_10IOA04 = "eletechsup_10ioa04"
    ENEREN_RER020I_EFHR0_EVO = "eneren_rer_020i"
    AERMEC_HMI080 = "aermec_hmi080"
    WAVESHARE_RTU_RELAY = "waveshare_rtu_relay"

# ADDRESS = 0
# QUANTITY = 1
# FUNCTION = 2
# DATA_TYPE = 3
# BLOCK_NAME = 0
# BLOCK_NDX = 1
# PRECISION = 2
# SCALE = 3
# STATE_CLASS = 4
# DEVICE_CLASS = 5
# UNIT_OF_MEASURE = 6
# SWITCH_STATE_OPEN = 5
# SWITCH_STATE_CLOSE = 4
# COMMAND_ADDRESS = 2
# COMMAND_WRITE_TYPE = 3
# COMMAND_OPEN = 5
# COMMAND_CLOSE = 4


# BLK_ADDRESS = 0
# BLK_QUANTITY = 1
# BLK_FUNCTION = 2
# BLK_DATA_TYPE = 3
# BLK_STATE_CLOSE = 4
# BLK_STATE_OPEN = 5

class BoardMetadataRegIdx(IntEnum):
    MANUFACTURER = 0
    MODEL = 1

class BoardBlockRegIdx(IntEnum):
    BLOCK_ADDRESS = 0
    BLOCK_QTY = 1
    BLOCK_FUNCTION = 2
    BLOCK_DEF_DATATYPE = 3

class SwitchRegIdx(IntEnum):
    BLOCK_STATE_OPEN = 5
    BLOCK_STATE_CLOSE = 4

    BLOCK_NAME = 0
    BLOCK_DATA_NDX = 1
    REGW_ADDRESS = 2
    REGW_FUNCTION = 3
    REGW_COMMAND_CLOSE = 4
    REGW_COMMAND_OPEN = 5
    GUIDE = 6

class NumericRegIdx(IntEnum):
    BLOCK_NAME = 0
    BLOCK_DATA_NDX = 1
    BLOCK_DATA_PRECISION = 2
    BLOCK_DATA_SCALE = 3
    BLOCK_DATA_DATATYPE = 4
    BLOCK_STATE_CLASS = 5
    BLOCK_DEVICE_CLASS = 6
    BLOCK_UNIT_OF_MEASURE = 7

    REGW_ADDRESS = 8
    REGW_FUNCTION = 9
    REGW_SCALE = 10

    SLIDER_MIN = 11
    SLIDER_MAX = 12
    SLIDER_STEP = 13
    SLIDER_MODE = 14
    GUIDE = 15

class SensorRegIdx(IntEnum):
    BLOCK_NAME = 0
    BLOCK_DATA_NDX = 1
    BLOCK_DATA_PRECISION = 2
    BLOCK_DATA_SCALE = 3

    BLOCK_STATE_CLASS = 4
    BLOCK_DEVICE_CLASS = 5
    BLOCK_UNIT_OF_MEASURE = 6
    GUIDE = 7

class BinarySensorRegIdx(IntEnum):
    BLOCK_NAME = 0
    BLOCK_DATA_NDX = 1
    BLOCK_DATA_PRECISION = 2
    BLOCK_DATA_SCALE = 3

    BLOCK_STATE_CLASS = 4
    BLOCK_DEVICE_CLASS = 5
    BLOCK_UNIT_OF_MEASURE = 6
    GUIDE = 7

# RBD_BLOCK_NAME = 0
# RBD_BLOCK_NDX = 1
# RBD_PRECISION = 2
# RBD_SCALE = 3
# RBD_STATE_CLASS = 4
# RBD_DEVICE_CLASS = 5
# RBD_UNIT_OF_MEASURE = 6
# RWBD_ADDRESS = 7
# RWBD_FUNCTION = 8
# RWBD_SCALE = 9
# RWBD_MIN = 10
# RWBD_MAX = 11
# RWBD_STEP = 12
# RWBD_NMODE = 13
# RWBD_GUIDE = 14

# WBD_BLOCK_NAME = 0
# WBD_BLOCK_NDX = 1
# WBD_ADDRESS = 2
# WBD_FUNCTION = 3
# WBD_COMMAND_CLOSE = 4
# WBD_COMMAND_OPEN = 5
# WBD_GUIDE = 6

XY_MOD01_SHT20_REGISTERS = {
# entity    0:manufacturer, 1:model
    METADATA: ("etc2", "xy mod01 sht20"),
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0001, 2, CALL_TYPE_REGISTER_INPUT, DataType.UINT16,             
        ),
        RN_TEMPERATURE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_HUMIDITY : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "humidity", "%"
        )
    }
}

GAUSELINK_TH02_PE_REGISTERS = {
# entity    0:manufacturer, 1:model
    METADATA: ("gauselink", "gl-th02-pe"),
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0000, 2, CALL_TYPE_REGISTER_INPUT, DataType.UINT16,             
        ),
        RN_TEMPERATURE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_HUMIDITY : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "humidity", "%"
        )
    }
}

SDM120M_REGISTERS = {
    METADATA: ("eastron", "sdm120m"),
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0000, 32, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32,             
        ),
        BoardBlock.REGISTERS_BLOCK_2 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0156, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32,             
        ),
        RN_VOLTAGE: (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "voltage", "V", 
        ),
        RN_CURRENT: (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 2, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "current", "A", 
        ),
        RN_ACTIVE_POWER: (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 1, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "power", "W", 
        ),
        RN_TOTAL_ACTIVE_ENERGY: (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_2, 0x00, 2, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "total", "energy", "kWh", 
        )
    }
}

R4D3B16_REGISTERS = {
    METADATA: ("eletechsup", "r4d3b16"),
    Platform.SWITCH : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:state close, 4:state open 
            0x0001, 16, CALL_TYPE_REGISTER_HOLDING, None, 0x0001, 0x0000,             
        ),
        RN_CHANNEL_00: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0x0001, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_01: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0x0002, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_02: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0x0003, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_03: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0x0004, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_04: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 0x0005, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_05: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 0x0006, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_06: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 0x0007, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_07: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 0x0008, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_08: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 0x0009, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_09: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x09, 0x000A, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_10: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0A, 0x000B, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_11: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0B, 0x000C, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_12: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 0x000D, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_13: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 0x000E, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_14: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 0x000F, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
        RN_CHANNEL_15: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 0x0010, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
        ),
    }
}

WAVESHARE_RTU_RELAY_REGISTERS = {
    METADATA: ("waveshare", "modbus_rtu_ralay"),
    Platform.SWITCH : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:state close, 4:state open 
            0x00FF, 1, CALL_TYPE_COIL, None, True, False,             
        ),
        RN_CHANNEL_00: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0x0000, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_01: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0x0001, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_02: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0x0002, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_03: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0x0003, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_04: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 0x0004, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_05: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 0x0005, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_06: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 0x0006, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
        RN_CHANNEL_07: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 0x0007, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
        ),
    }
}

E10IOA04_REGISTERS = {
    METADATA: ("eletechsup", "10ioa04"),
    Platform.SWITCH : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:state close, 4:state open 
            0x0000, 4, CALL_TYPE_COIL, None, True, False,             
        ),
        RN_CHANNEL_00: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0x0000, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
        ),
        RN_CHANNEL_01: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0x0001, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
        ),
        RN_CHANNEL_02: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0x0002, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
        ),
        RN_CHANNEL_03: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0x0003, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
        ),
    }
}

NT18B07_REGISTERS = {
# entity    0:manufacturer, 1:model
    METADATA: ("eletechsup", "nt18b07"),
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0000, 7, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16,             
        ),
        RN_CHANNEL_00 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_01 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_02 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_03 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_04 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_05 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RN_CHANNEL_06 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
    }
}

N4DBA06_REGISTERS = {
# entity    0:manufacturer, 1:model
    METADATA: ("eletechsup", "n4dba06"),
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0000, 4, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16,             
        ),
        RN_VIN2_VALUE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.01,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "voltage", "V"
        ),
        RN_VIN2_VALUE_PERCENTAGE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, "%"
        ),
    },
    Platform.NUMBER : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x0080, 4, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16,             
        ),
        RN_VOUT2_VALUE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "voltage", "V",
# write     7:address, 8:function, 9:scale
            0x0081, CALL_TYPE_WRITE_REGISTER, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 10, 0.5, MODE_BOX,
        ),
        RN_VOUT2_VALUE_PERCENTAGE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, "%",
# write     7:address, 8:function, 9:scale
            0x0081, CALL_TYPE_WRITE_REGISTER, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 100, 1, MODE_BOX,
        ),       
    }
}

RER020I_EFHR0_EVO_REGISTERS = {
    METADATA: ("eneren", "rer_020i"),
    Platform.BINARY_SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x00, 26, CALL_TYPE_DISCRETE, DataType.UINT16,             
        ), 
        RER_PRESENZA_ALLARME : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_AVVERTIMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_FILTRI_DA_PULIRE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_MANCANZA_COMUNICAZIONE_CON_DISPLAY : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_OPZIONE_SERRANDE_ESTERNE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_OPZIONE_SBRINAMENTO_RECUPERATORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_FREE_COOLING : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x09, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_ALLARME_SONDA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0A, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_ALLARME_SONDA_CO2_AMBIENTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0B, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_ALLARME_ALTA_PRESSIONE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_AVVERTIMENTO_BASSA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_AVVERTIMENTO_ALTA_TEMPERATURA_ACQUA_PER_ON_COMPRESSORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_AVVERTIMENTO_RISCHIO_CONGELAMENTO_BATTERIA_ACQUA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_ALLARME_DEW_POINT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_STATO_COMPRESSORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x11, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_STATO_FREE_COOLING : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x12, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_RICHIESTA_ACQUA_DA_IMPIANTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x13, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_RICHIESTA_DEUMIDIFICA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x14, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_RICHIESTA_RAFFREDDAMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x15, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_RICHIESTA_RISCALDAMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x16, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_SONDA_T_MANDATA_ARIA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x17, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_CONTROLLO_TEMPERATURA_MANDATA_ONOFF_ATTIVO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x18, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        RER_PRESENZA_FUNZIONE_CONTROLLO_TEMPERATURA_DI_MANDATA_MODULANTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x19, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
    },
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x00, 28, CALL_TYPE_REGISTER_INPUT, DataType.UINT16,             
        ),
        RER_TEMPERATURA_AMBIENTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),      
        RER_UMIDITA_RELATIVA_AMBIENTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "humidity", "%"
        ),
        RER_SONDA_CO2 : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "co2", "ppm"
        ),
# ...
        RER_TEMPERATURA_ACQUA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RER_TEMPERATURA_ESTERNA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x11, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ),
        RER_STATO_VENTILATORE_MANDATA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x12, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", None, "%"
        ), 
        RER_STATO_VENTILATORE_ESTRAZIONE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x13, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", None, "%"
        ),
        RER_SET_TEMPERATURE_EFFETTIVO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x14, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C"
        ), 
        RER_SET_UMIDITA_EFFETTIVO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x15, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "humidity", "%"
        ), 
        RER_SET_RICAMBIO_EFFETTIVO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x16, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", None, None
        ), 
        RER_ORE_FUNZIONAMENTO_UNITA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x17, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", None, None
        ),
        RER_RELEASE_SOFTWARE_SCHEDA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x18, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", None, None
        ),
        RER_TEMPERATURA_MANDATA_ARIA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x19, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
           "measurement", "temperature", "°C"
        ), 
    },
    Platform.SWITCH : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:state close, 4:state open 
            0x00, 24, CALL_TYPE_COIL, None, 0x01, 0x00,             
        ),    
        RER_DEVICE_POWER_CONTROL: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0x00, CALL_TYPE_WRITE_COILS, 0x01, 0x00
#           6:guide
        ),
        RER_STAGIONE: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0x01, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
            "0. estate, 1. inverno"
        ),    
        RER_FORZATURA_OFF_TRATTAMENTO: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0x02, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),    
        RER_RESET_ALLARMI: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0x03, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),    
        RER_RESET_PULIZIA_FILTRI: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 0x04, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),    
        RER_ABILITAZIONE_FORZATURA_FREE_COOLING: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 0x08, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),    
        RER_FORZATURA_FREE_COOLING: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x09, 0x09, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),
        RER_FORZATURA_RISCALDAMENTO: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 0x0C, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),
        RER_FORZATURA_RAFFREDDAMENTO: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 0x0D, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),
        RER_ABILITAZIONE_FORZATURA_DEUMIDIFICA_UMIDIFICA: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 0x0E, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),
        RER_FORZATURA_DEUMIDIFICA: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 0x0F, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
        ),
        RER_RICHIESTA_VENTILAZIONE_DI_RICIRCOLO: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 0x10, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
            "Solo se non sono attive richieste di trattamento o altre funzioni di protezione"
        ),
        RER_UNITA_MISURA_TEMPERATURA: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x11, 0x11, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
            "0. Gradi celsius, 1. Gradi fahrenheit"
        ),
        RER_GESTIONE_CONTROLLO_TEMPERATURA_MANDATA: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x15, 0x15, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
            "0. Utilizzo della sonda di temperatura mandata (se presente opzione controllo di temperatura di mandata modulante), 1. Utilizzo della sonda di temperatura ambiente"
        ),
        RER_GESTIONE_CONTROLLO_DEW_POINT: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x16, 0x16, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
#           6:guide
            "0. Dew-point variabile (T superficiale = T acqua + differenziale. La T acqua viene misurata dalla macchina; differenziale e T dew-point sono parametri impostabili), 1. Dew-point fisso (T superficiale)"
        ),
    },
    Platform.NUMBER : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x00, 21, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16,              
        ), 
        RER_SET_TEMPERATURE_AMBIENTE_IN_CENSIUS : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x00, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            15, 30, 0.1, MODE_BOX,
        ),
        RER_SET_UMIDITA_RELATIVA_AMBIENTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "humidity", "%",
# write     7:address, 8:function, 9:scale
            0x01, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            40, 90, 0.1, MODE_BOX,
        ),
        RER_SET_RICAMBIO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x02, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 5, 1, MODE_BOX,
        ),
        RER_OROLOGIO_ORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x03, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 23, 1, MODE_BOX,
        ),
        RER_OROLOGIO_MINUTI : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x04, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 59, 1, MODE_BOX,
        ),
        RER_OROLOGIO_GIORNO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x05, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 31, 1, MODE_BOX,
        ),
        RER_OROLOGIO_MESE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x06, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 12, 1, MODE_BOX,
        ),
        RER_OROLOGIO_ANNO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x07, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            10, 99, 1, MODE_BOX,
        ),
        RER_OROLOGIO_GIORNO_DELLA_SETTIMANA : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x08, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 6, 1, MODE_BOX,
        ),
        RER_FORZATURA_VALVOLA_ACQUA_MODULANTE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0A, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, "%",
# write     7:address, 8:function, 9:scale
            0x0A, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 100, 1, MODE_BOX,
        ),
        RER_TEMPERATURA_MINIMA_INVERNALE_SENZA_RISCALDAMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0B, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0B, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 90, 1, MODE_BOX,
        ),
        RER_TEMPERATURA_MASSIMA_ESTIVA_SENZA_RAFFREDDAMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0C, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 90, 1, MODE_BOX,
        ),
        RER_GESTIONE_RAFFREDDAMENTO : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x0D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 2, 1, MODE_BOX,
            "0. Utilizzo del solo compressore, 1. Utilizzo solo dell'acqua, 2. Prima dell'acqua, se non sufficiente compressore",
        ),
        RER_PROTEZIONE_DEW_POINT_DIFFERENZIALE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0E, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            -10, 10, 1, MODE_BOX,
        ),
        RER_PROTEZIONE_DEW_POINT_VALORE_T_DEW_POINT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 1, 0.1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0F, CALL_TYPE_WRITE_REGISTERS, 10,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            10, 40, 0.1, MODE_BOX,
        ),
        RER_ORE_ATTESA_PROMEMORIA_PULIZIA_FILTRI_SPORCHI : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x10, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            720, 4320, 0.1, MODE_BOX,
        ),
        RER_RICHIESTA_ATTIVAZIONE_COMPRESSORE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x13, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x13, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 2, 1, MODE_BOX,
            "0. Deumidifica o raffreddamento, 1. Solo deumidifica, 2. Solo raffreddamento",
        ),
    }
}

AERMEC_HMI080_REGISTERS = {
    METADATA: ("aermec", "hmi080"),
    Platform.BINARY_SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x00, 198, CALL_TYPE_COIL, DataType.UINT16,             
        ),   
        HMI080_HEAT_2_WAY_VALVE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x26, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_IDU : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x40, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),    
        HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_ODU : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x41, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),    
        HMI080_COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_DRIVE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x42, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_HP_ANTIFREE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x43, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_COMPRESSOR_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x50, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_ODU_FAN_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x51, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_4_WAY_VALVE_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x53, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_COMPRESSOR_CRANKCASE_HEATER_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x54, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_UNDERPAN_HEATER_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x55, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DEFROSTING_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x56, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_OIL_RETURN_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x57, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_AMBIENT_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x58, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DEFROST_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x59, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DISCHARGE_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5A, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_SUCTION_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5B, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_ODU_FAN_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5C, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_HIGH_PRESSURE_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5D, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_HIGH_PRESSURE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5E, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_LOW_PRESSURE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x5F, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_HIGH_DISCHARGE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x60, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_CAPACITY_DIP_SETTING_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x61, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_COMMUNICATION_ERROR_BETWEEN_IDU_AND_ODU : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x62, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_ECONOMIZER_IN_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x63, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_ECONOMIZER_OUT_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x64, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_SYSTEM_RECOVERABLE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x66, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_SYSTEM_IRRECOVERABLE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x67, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_FLOW_SWITCH_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x6C, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DC_BUS_LOW_VOLTAGE_OR_VOLTAGE_DROP : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x80, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DC_BUS_OVER_VOLTAGE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x81, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_AC_CURRENT_PROTECTION_INPUT_SIDE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x82, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_IPM_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x83, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_PFC_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x84, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_STARTUP_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x85, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_PHASE_LOSS : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x86, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DRIVE_MODULE_RESETTING : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x87, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_COMPRESSOR_OVERCURRENT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x88, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_OVER_SPEED : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x89, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_CHARGING_CIRCUIT_ERROR_OR_CURRENT_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8A, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),  
        HMI080_DESYNCHRONIZING : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8B, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_COMPRESSOR_STALLING : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8C, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_DRIVE_COMMUNICATION_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8D, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_RADIATOR_OR_IPM_OR_PFC_OVER_TEMPERATURE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8E, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_DEFECTIVE_RADIATOR_OR_IPM_OR_PFC : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x8F, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_CHARGING_CIRCUIT_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x92, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_AC_INPUT_VOLTAGE_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x93, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_DRIVE_BOARD_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x94, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_AC_CONTACTOR_PROTECTION_OR_INPUT_CROSS_ZERO_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x95, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_TEMP_DRIFT_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x96, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_SENSOR_CONNECTION_PROTECTION_CONNN : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x97, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_CONDENSER_LEAVING_WATER_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x98, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_E_HEATER_LEAVING_WATER_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x99, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),        
        HMI080_REFRIGERANT_LIQUID_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x9A, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_CONDENSER_ENTERING_WATER_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x9B, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_WATER_TANK_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x9C, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_REFRIGERANT_VAPOR_LINE_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x9E, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_REMOTE_ROOM_TEMP_SENSOR_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xA0, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_OTHER_HEAT_SOURCE_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xA9, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_FLOW_SWITCH_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xAA, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_IDU_E_HEATER_1_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xAB, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_IDU_E_HEATER_2_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xAC, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_WATER_TANK_HEATER_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xAD, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_IDU_WATER_PUMP_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xAF, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_CIRCULATING_2_WAY_VALVE_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB0, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_PLATE_HEATER_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB1, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_3_WAY_VALVE_STATE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB2, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_GATE_CTRL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB3, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_JUMPER_CAP_ERROR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB8, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_E_HEATER_1_WELDING_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xB9, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_E_HEATER_2_WELDING_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xBA, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_WATER_HEATER_WELDING_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xBB, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_WATER_FLOW_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xBC, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_IDU_RECOVERABLE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xBE, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_IDU_IRRECOVERABLE_PROTECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0xBF, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
    },
    Platform.SENSOR : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x75, 21, CALL_TYPE_REGISTER_HOLDING, DataType.INT16,      
        ),    
        HMI080_UNIT_STATUS : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
            "01. Cool, 02. Heat, 06. Hot water, 08. Off"
        ),    
        HMI080_T_OUTDOOR : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_DISCHARGE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_DEFROST : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_SUCTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_ECONOMIZER_IN : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_ECONOMIZER_OUT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_DIS_PRESSURE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_WATER_OUT_PE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_OPTIONAL_WATER_SENS : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x09, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_WATER_IN_PE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0A, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_TANK_CTRL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0B, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_REMOTE_ROOM : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_GAS_PIPE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_T_LIQUID_PIPE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_THERMOSTAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
            "1. Cool, 2. Heat, 3. Off"
        ),
        HMI080_T_FLOOR_DEBUG : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),
        HMI080_DEBUG_TIME : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x11, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_DISINFECTION : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x12, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_ERROR_TIME_FOR_FLOOR_DEBUG : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x13, 0, 1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None
        ),
        HMI080_T_WEATHER_DEPEND : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x14, 1, 0.1,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
        ),        
    },
    Platform.SWITCH : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:state close, 4:state open 
            0x2A, 2, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 0xAA, 0x55,  
        ),
        BoardBlock.REGISTERS_BLOCK_2 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x00, 199, CALL_TYPE_COIL, DataType.UINT8,             
        ),    
        HMI080_DEVICE_POWER_CONTROL: (
#           0:block_name, 1:index, 2:address, 3:function, 4:open, 5:close
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0x002A, CALL_TYPE_WRITE_REGISTERS, 0xAA, 0x55
#           6:guide
        ),
        HMI080_RW_WEEKLY_TIMER: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x08, 0x08, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_CLOCK_TIMER: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x09, 0x09, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_TEMP_TIMER: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x0A, 0x0A, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_GATE_CTRL: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x0B, 0x0B, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_SOLAR_HEATER: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x10, 0x10, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_CTRL_STATE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x11, 0x11, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_FAST_HOT_WATER: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x12, 0x12, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_COOL_AND_HOT_WATER_PRIORITY: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x13, 0x13, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_HEAT_AND_HOT_WATER_PRIORITY: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x14, 0x14, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_QUITE_MODE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x15, 0x15, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_WEATHER_DEPEND: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x16, 0x16, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_DISINFECTION: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x17, 0x17, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_FLOOR_DEBUG: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x18, 0x18, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_FLOOR_DEBUG_START_STOP: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x19, 0x19, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_EMERGENCE_MODE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x1A, 0x1A, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_EMERGENCE_MODE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x1A, 0x1A, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_OTHER_THERMAL: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x1B, 0x1B, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_WATER_TANK: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x1D, 0x1D, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_SOLAR_SETTING: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x1F, 0x1F, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_REMOTE_SENSOR: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x21, 0x21, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_HOLIDAY_MODE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x22, 0x22, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_REFRI_RECOVERY: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x23, 0x23, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_MANUAL_DEFROST: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x24, 0x24, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
        HMI080_RW_COOL_2_WAY_VALVE: (
#           0:block_name, 1:index, 2:address, 3:function, 5:close, 4:open
            BoardBlock.REGISTERS_BLOCK_2, 0x25, 0x25, CALL_TYPE_WRITE_COILS, True, False
#           6:guide
        ),
    },
    Platform.NUMBER : {
        BoardBlock.REGISTERS_BLOCK_1 : (
# read      0:address, 1:quantity, 2:function, 3:data_type 
            0x02, 40, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16,              
        ),
        HMI080_MODE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x00, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x02, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 5, 1, MODE_BOX,
            "1. Heat, 2. Hot water, 3. Cool + Heat water, 4. Heat + Hot water, 5. Cool",
        ),
        HMI080_OPTIONAL_E_HEATER : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x01, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x03, CALL_TYPE_WRITE_REGISTERS, 1, None,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 3, 1, MODE_BOX,
            "1. 1 set, 2. 2 sets, 3. Off, Default: 1 set",
        ),
        HMI080_DISINFECTION_TEMP : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x02, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x04, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            40, 70, 1, MODE_BOX,
        ),
        HMI080_FLOR_DEBUG_SEGMENTS : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x03, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x05, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 10, 1, MODE_BOX,
        ),
        HMI080_FLOR_DEBUG_PERIOD_1_TEMP : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x04, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x06, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            25, 35, 1, MODE_BOX,
        ),
        HMI080_DELTA_T_OF_SEGMENT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x05, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x07, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            2, 10, 1, MODE_BOX,
        ),
        HMI080_SEGMENT_TIME : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x06, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x08, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            12, 72, 1, MODE_BOX,
        ),
        HMI080_WOT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x07, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x09, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            7, 25, 1, MODE_BOX,
        ),
        HMI080_WOT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x08, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0A, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            20, 55, 1, MODE_BOX,
        ),
        HMI080_RT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x09, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0B, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            20, 60, 1, MODE_BOX,
        ),
        HMI080_RT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0A, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0C, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            18, 30, 1, MODE_BOX,
        ),
        HMI080_T_WATER_TANK : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0B, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            40, 80, 1, MODE_BOX,
        ),
        HMI080_T_EHEATER : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0C, 0, 1, DataType.INT16,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0E, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            -20, 18, 1, MODE_BOX,
        ),
        HMI080_T_OTHER_SWITCH_ON : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0D, 0, 1, DataType.INT16,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x0F, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            -20, 18, 1, MODE_BOX,
        ),
        HMI080_T_HP_MAX : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0E, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x10, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            40, 55, 1, MODE_BOX,
        ),
        HMI080_UPPER_AT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x0F, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x11, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            10, 37, 1, MODE_BOX,
        ),
        HMI080_LOWER_AT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x10, 0, 1, DataType.INT16,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x12, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            -20, 9, 1, MODE_BOX,
            "Default: -20°C"
        ),
        HMI080_UPPER_RT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x11, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x13, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            22, 30, 1, MODE_BOX,
        ),
        HMI080_LOWER_RT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x12, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x14, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            18, 21, 1, MODE_BOX,
        ),
        HMI080_UPPER_WT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x13, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x15, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            46, 60, 1, MODE_BOX,
        ),
        HMI080_LOWER_WT_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x14, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x16, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            36, 45, 1, MODE_BOX,
        ),
        HMI080_UPPER_AT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x15, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x17, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            26, 48, 1, MODE_BOX,
        ),
        HMI080_LOWER_AT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x16, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x18, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            10, 25, 1, MODE_BOX,
            "Default: 25 °C"
        ),
        HMI080_UPPER_RT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x17, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x19, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            24, 30, 1, MODE_BOX,
        ),
        HMI080_LOWER_RT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x18, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1A, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            18, 23, 1, MODE_BOX,
        ),
        HMI080_UPPER_WT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x19, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1B, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            15, 25, 1, MODE_BOX,
        ),
        HMI080_LOWER_WT_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1A, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1C, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            7, 14, 1, MODE_BOX,
        ),
        HMI080_DELTA_T_COOL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1B, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            2, 10, 1, MODE_BOX,
        ),
        HMI080_DELTA_T_HEAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1C, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1E, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            2, 10, 1, MODE_BOX,
        ),
        HMI080_DELTA_T_HOT_WATER : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1D, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x1F, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            2, 10, 1, MODE_BOX,
        ),
        HMI080_DELTA_T_ROOM_TEMP : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1E, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            "measurement", "temperature", "°C",
# write     7:address, 8:function, 9:scale
            0x20, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 5, 1, MODE_BOX,
        ),
        HMI080_COOL_RUN_TIME : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x1F, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x21, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 10, 1, MODE_BOX,
        ),
        HMI080_HEAT_RUN_TIME : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x20, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x22, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 10, 1, MODE_BOX,
            "Default: 5 min"
        ),
        HMI080_OTHER_THERMAL_LOGIC : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x21, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x23, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 3, 1, MODE_BOX,
        ),
        HMI080_TANK_HEATER : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x22, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x24, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 2, 1, MODE_BOX,
        ),
        HMI080_OPTIONAL_E_HEATER_LOGIC : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x23, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x25, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 2, 1, MODE_BOX,
        ),
        HMI080_CURRENT_LIMIT_VALUE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x24, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x26, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 50, 1, MODE_BOX,
        ),
        HMI080_RW_THERMOSTAT : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x25, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x27, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            0, 2, 1, MODE_BOX,
            "0. Without, 1. Air, 2. Air + hot water, Default: Without"
        ),
        HMI080_FORCE_MODE : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x26, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x28, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 3, 1, MODE_BOX,
            "1. Force-cool, 2. Force-heat, 3. Off, Default: Off"
        ),
        HMI080_AIR_REMOVAL : (
#           0:block_name, 1:index, 2:precision, 3:scale
            BoardBlock.REGISTERS_BLOCK_1, 0x27, 0, 1, None,
# entity    4:state_class, 5:device_class, 6:unit_of_measurement
            None, None, None,
# write     7:address, 8:function, 9:scale
            0x29, CALL_TYPE_WRITE_REGISTERS, 1,
# number    10:min, 11:max, 12:step, 13:mode (auto, box, slider)
            1, 3, 1, MODE_BOX,
            "1. Air, 2. Water tank, 3. Off, Default: Off"
        ),
    }
}

BOARDS = {
    Board.AERMEC_HMI080: AERMEC_HMI080_REGISTERS,
    Board.EASTRON_SDM120M: SDM120M_REGISTERS,
    Board.ENEREN_RER020I_EFHR0_EVO: RER020I_EFHR0_EVO_REGISTERS,
    Board.ELETECHSUP_10IOA04: E10IOA04_REGISTERS,
    Board.ELETECHSUP_N4DBA06: N4DBA06_REGISTERS,
    Board.ELETECHSUP_NT18B07: NT18B07_REGISTERS,
    Board.ELETECHSUP_R4D3B16: R4D3B16_REGISTERS,
    Board.WAVESHARE_RTU_RELAY : WAVESHARE_RTU_RELAY_REGISTERS,
    Board.XY_MOD01_SHT20: XY_MOD01_SHT20_REGISTERS,
    Board.GL_TH02_PE : GAUSELINK_TH02_PE_REGISTERS,
}


