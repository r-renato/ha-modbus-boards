"""Constants used in modbus integration."""
from enum import Enum
from enum import StrEnum

from homeassistant.const import (
    CONF_ADDRESS,
    CONF_BINARY_SENSORS,
    CONF_COVERS,
    CONF_LIGHTS,
    CONF_SENSORS,
    CONF_SWITCHES,
    Platform,
)

# configuration names
CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_CLIMATES = "climates"
CONF_CLOSE_COMM_ON_ERROR = "close_comm_on_error"
CONF_DATA_TYPE = "data_type"
CONF_DEVICE_ADDRESS = "device_address"
CONF_FANS = "fans"
CONF_INPUT_TYPE = "input_type"
CONF_LAZY_ERROR = "lazy_error_count"
CONF_MAX_TEMP = "max_temp"
CONF_MAX_VALUE = "max_value"
CONF_MIN_TEMP = "min_temp"
CONF_MIN_VALUE = "min_value"
CONF_MSG_WAIT = "message_wait_milliseconds"
CONF_NAN_VALUE = "nan_value"
CONF_NUMBERS = "numbers"
CONF_PARITY = "parity"
CONF_RETRIES = "retries"
CONF_RETRY_ON_EMPTY = "retry_on_empty"
CONF_PRECISION = "precision"
CONF_SCALE = "scale"
CONF_SLAVE_COUNT = "slave_count"
CONF_STATE_CLOSED = "state_closed"
CONF_STATE_CLOSING = "state_closing"
CONF_STATE_OFF = "state_off"
CONF_STATE_ON = "state_on"
CONF_STATE_OPEN = "state_open"
CONF_STATE_OPENING = "state_opening"
CONF_STATUS_REGISTER = "status_register"
CONF_STATUS_REGISTER_TYPE = "status_register_type"
CONF_STEP = "temp_step"
CONF_STOPBITS = "stopbits"
CONF_SWAP = "swap"
CONF_SWAP_BYTE = "byte"
CONF_SWAP_NONE = "none"
CONF_SWAP_WORD = "word"
CONF_SWAP_WORD_BYTE = "word_byte"
CONF_TARGET_TEMP = "target_temp_register"
CONF_TARGET_TEMP_WRITE_REGISTERS = "target_temp_write_registers"
CONF_HVAC_MODE_REGISTER = "hvac_mode_register"
CONF_HVAC_MODE_VALUES = "values"
CONF_HVAC_ONOFF_REGISTER = "hvac_onoff_register"
CONF_HVAC_MODE_OFF = "state_off"
CONF_HVAC_MODE_HEAT = "state_heat"
CONF_HVAC_MODE_COOL = "state_cool"
CONF_HVAC_MODE_HEAT_COOL = "state_heat_cool"
CONF_HVAC_MODE_AUTO = "state_auto"
CONF_HVAC_MODE_DRY = "state_dry"
CONF_HVAC_MODE_FAN_ONLY = "state_fan_only"
CONF_WRITE_REGISTERS = "write_registers"
CONF_VERIFY = "verify"
CONF_VIRTUAL_COUNT = "virtual_count"
CONF_WRITE_TYPE = "write_type"
CONF_ZERO_SUPPRESS = "zero_suppress"

RTUOVERTCP = "rtuovertcp"
SERIAL = "serial"
TCP = "tcp"
UDP = "udp"


# service call attributes
ATTR_ADDRESS = CONF_ADDRESS
ATTR_HUB = "hub"
ATTR_UNIT = "unit"
ATTR_SLAVE = "slave"
ATTR_VALUE = "value"


class DataType(str, Enum):
    """Data types used by sensor etc."""

    CUSTOM = "custom"
    STRING = "string"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    UINT64 = "uint64"
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    FLOAT64 = "float64"

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

# call types
CALL_TYPE_COIL = "coil"
CALL_TYPE_DISCRETE = "discrete_input"
CALL_TYPE_REGISTER_HOLDING = "holding"
CALL_TYPE_REGISTER_INPUT = "input"
CALL_TYPE_WRITE_COIL = "write_coil"
CALL_TYPE_WRITE_COILS = "write_coils"
CALL_TYPE_WRITE_REGISTER = "write_register"
CALL_TYPE_WRITE_REGISTERS = "write_registers"
CALL_TYPE_X_COILS = "coils"
CALL_TYPE_X_REGISTER_HOLDINGS = "holdings"

# service calls
SERVICE_WRITE_COIL = "write_coil"
SERVICE_WRITE_REGISTER = "write_register"
SERVICE_STOP = "stop"
SERVICE_RESTART = "restart"

# dispatcher signals
SIGNAL_STOP_ENTITY = "modbus.stop"
SIGNAL_START_ENTITY = "modbus.start"

# integration names
DEFAULT_HUB = "modbus_hub"
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_SLAVE = 1
DEFAULT_STRUCTURE_PREFIX = ">f"
DEFAULT_TEMP_UNIT = "C"
MODBUS_DOMAIN = "modbus"

ACTIVE_SCAN_INTERVAL = 2  # limit to force an extra update

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

###
### My code
###
MODBUS_DOMAIN = "drp_modbus_boards"
DEFAULT_NAME = "drp_modbus_boards"
DEFAULT_HUB = "drp_modbus_boards_hub"
DEFAULT_MODBUS_ADDRESS = 1

CONF_INITIAL = "initial"

CONF_MODBUS_ADDRESS = "modbus_address"
CONF_BOARD_DEVICE = "device"
CONF_BOARD = "board"
CONF_REVERSE = "reverse"
CONF_SWITCH_CONSTRAINT = "switch_constraint"


MODE_SLIDER = "slider"
MODE_BOX = "box"

class Board(StrEnum):
    """Available entity Board."""

    EASTRON_SDM120M = "eastron_sdm120m"
    ELETECHSUP_NT18B07 = "eletechsup_nt18b07"
    ELETECHSUP_N4DBA06 = "eletechsup_n4dba06"
    ELETECHSUP_R4D3B16 = "eletechsup_r4d3b16"
    ELETECHSUP_10IOA04 = "eletechsup_10ioa04"
    ENEREN_RER020I_EFHR0_EVO = "eneren_rer_020i"
    AERMEC_HMI080 = "aermec_hmi080"
    WAVESHARE_RTU_RELAY = "waveshare_rtu_relay"

class SDM120MSensor(StrEnum):
    """Available entity SDM120M Sensor."""

    VOLTAGE = "voltage"
    CURRENT = "current"
    POWER_ACTIVE = "power_active"
    POWER_APPARENT = "power_apparent"

WAVESHARE_RTU_RELAY_REGISTERS = {
    Platform.SWITCH : {
        "relay_channel_01": (
# read      0:address, 1:function, 2:open, 3:close 
            0x00FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0000, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 1)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_02": (
# read      0:address, 1:function, 2:open, 3:close 
            0x01FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0001, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 2)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_03": (
# read      0:address, 1:function, 2:open, 3:close 
            0x02FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0002, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 3)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_04": (
# read      0:address, 1:function, 2:open, 3:close 
            0x03FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0003, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 4)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_05": (
# read      0:address, 1:function, 2:open, 3:close 
            0x04FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0004, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 5)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_06": (
# read      0:address, 1:function, 2:open, 3:close 
            0x05FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0005, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 6)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_07": (
# read      0:address, 1:function, 2:open, 3:close 
            0x06FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0006, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 7)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
        "relay_channel_08": (
# read      0:address, 1:function, 2:open, 3:close 
            0x07FF, CALL_TYPE_COIL, 0xFF00, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0007, CALL_TYPE_WRITE_COIL, 0xFF00, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 8)",
# entity    9:manufacturer, 10:model            
            "waveshare", "modbus_rtu_ralay"), 
    },
}

AERMEC_HMI080_REGISTERS = {
    Platform.BINARY_SENSOR : {
        "compressor_state": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x50, 1, CALL_TYPE_COIL, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Compressor state",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),
        "odu_fan_state": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x51, 1, CALL_TYPE_COIL, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "ODU Fan State",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),
    },
    Platform.SWITCH : {
        "device_power_control": (
# read      0:address, 1:function, 2:open, 3:close 
            0x002A, CALL_TYPE_REGISTER_HOLDING, 0xAA, 0x55,
# write     4:address, 5:function, 6:open, 7:close
            0x002A, CALL_TYPE_WRITE_REGISTERS, 0xAA, 0x55,
# entity    8:default_label
            "Device Powe Control",
# entity    9:manufacturer, 10:model            
            "aermec", "hmi080"), 
    },
    Platform.SENSOR : {
        "unit_status": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0075, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Unit Status",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),
        "temperature_outdoor": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0076, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Outdoor",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_discharge": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0077, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Discharge",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_defrost": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0078, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Defrost",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_suction": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0079, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Suction",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_economizer_in": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007A, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Economizer In",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"), 
        "temperature_economizer_out": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007B, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Economizer Out",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "dis_pressure": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007C, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Dis. pressure",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_water_out_pe": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007D, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature Water Out PE",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_optional_water_sen": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007E, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-optional water sen",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_water_in_pe": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x007F, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-water in PE",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_tank_ctrl": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0080, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-tank ctrl",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_remote_room": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0081, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-remote room",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_gas_pipe": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0082, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-gas pipe",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_liquid_pipe": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0083, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-liquid pipe",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_thermostat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0084, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             None, None, None, "Thermostat",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),    
        "temperature_t_floor_debug": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0085, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             "measurement", "temperature", "°C", "Temperature T-floor debug",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),   
        "debug_time": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0086, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             None, None, None, "Debug time",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),   
        "disinfection": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0087, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             None, None, None, "Disinfection",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),   
        "error_time_for_floor_debug": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0088, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             None, None, None, "Error Time for Floor Debug",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),   
        "temperature_t_weather_depend": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0089, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
             None, None, None, "Temperature T-weather depend",
# entity    10:manufacturer, 11:model
            "aermec", "hmi080"),   


    },
    Platform.NUMBER : {
        "operational_mode": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0002, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0002, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 5, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational mode",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_optional_e_heater": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0003, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0003, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 3, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Optional E-Heater",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_disinfection_temp": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0004, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0004, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            40, 70, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Disinfection Temp",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),  
        "operational_floor_debug_segments": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0005, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0005, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Floor Debug Segments",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_floor_debug_period_1_temp": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0006, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0006, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            25, 35, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Floor Debug Period 1 Temp",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_delta_t_of_segment": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0007, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0007, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            2, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Delta T of segment",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_segment_time": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0008, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0008, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            12, 72, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Segment Time",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_wot_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0009, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0009, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            7, 25, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational WOT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_wot_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000A, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000A, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            20, 55, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational WOT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_rt_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000B, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000B, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            20, 60, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational RT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_rt_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000C, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000C, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            18, 30, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational RT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_t_water_tank": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000D, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            40, 80, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational T-water tank",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_t_eheater": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000E, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000E, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            -20, 18, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational T-Eheater",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_t_other_switch_on": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000F, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x000F, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            -20, 18, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational T-Other switch on",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_t_hp_max": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0010, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0010, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            40, 55, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational T-HP max",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_at_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0011, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0011, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            10, 37, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper AT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_at_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0012, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0012, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            -20, 9, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower AT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_rt_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0013, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0013, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            22, 30, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper RT-Heats",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_rt_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0014, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0014, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            18, 21, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower RT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_wt_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0015, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0015, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            46, 60, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper WT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_wt_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0016, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0016, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            36, 45, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower WT-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_at_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0017, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0017, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            26, 48, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper AT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_at_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0018, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0018, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            10, 25, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower AT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_rt_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0019, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0019, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            24, 30, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper RT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_rt_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001A, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001A, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            18, 23, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower RT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_upper_wt_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001B, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001B, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            15, 25, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Upper WT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_lower_wt_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001C, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001C, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            7, 14, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Lower WT-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_delta_t_cool": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001D, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            2, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Delta-T-Cool",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_delta_t_heat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001E, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001E, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            2, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Delta-T-Heat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_delta_t_hot_water": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x001F, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x001F, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            2, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Delta-T-hot water",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_delta_t_room_temp": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0020, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0020, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 5, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Operational Delta-T-Room temp",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_cool_run_time": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0021, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0021, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Cool run time",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_heat_run_time": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0022, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0022, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 10, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Heat run time",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_other_thermal_logic": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0023, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0023, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 3, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Other thermal logic",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_tank_heater": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0024, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0024, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 2, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Tank heater",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_optional_e_heaterlogic": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0025, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0025, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 2, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Optional E-Heaterlogic",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_current_limit_value": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0026, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0026, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 50, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "current", "A", "Operational Current limit value",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_thermostat": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0027, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0027, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 2, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Thermostat",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_force_mode": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0028, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0028, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 3, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Force mode",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),
        "operational_air_removal": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0029, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0029, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            1, 3, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational Air removal",
# entity    17:manufacturer, 18:model
            "aermec", "hmi080"),

    }   
}

RER020I_EFHR0_EVO_REGISTERS = {
    Platform.BINARY_SENSOR : {
        "ro_presenza_allarme": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x00, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Presenza allarme",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_presenza_avvertimento": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x01, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Presenza avvertimento",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_filtri_da_pulire": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x02, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Filtri da pulire",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_presenza_free_cooling": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x09, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Presenza free-cooling",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_allarme_alta_pressione": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0C, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Allarme alta pressione",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_avvertimento_bassa_temperatura_acqua_per_on_compressore": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0D, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Avvertimento bassa temperatura acqua per ON compressore",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_avvertimento_alta_temperatura_acqua_per_on_compressore": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0E, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Avvertimento alta temperatura acqua per ON compressore",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_allarme_dew_point": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x10, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Allarme dew-point",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_stato_compressore": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x11, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Stato compressore",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_stato_free_cooling": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x12, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Stato free-cooling",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_richiesta_acqua_da_impianto": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x13, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Richiesta acqua da impianto",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_richiesta_deumidifica": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x14, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Richiesta deumidifica",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_richiesta_raffreddamento": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x15, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Richiesta raffreddamento",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_richiesta_riscaldamento": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x16, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Richiesta riscaldamento",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_presenza_sonda_t_mandata_aria": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x17, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Presenza sonda T mandata aria",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_controllo_temperatura_di_mandata_onoff_attivo": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x18, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Controllo temperatura di mandata on/off attivo",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_controllo_temperatura_di_mandata_onoff_attivo": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x19, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Controllo temperatura di mandata on/off attivo",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
        "ro_presenza_funzione_controllo_di_temperatura_di_mandata_modulante": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x1A, 1, CALL_TYPE_DISCRETE, DataType.UINT16, 0, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, None, "Presenza funzione controllo di temperatura di mandata modulante",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),    
    },
    Platform.SENSOR : {
        "ro_temperatura_ambiente": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x00, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Ambient Temperature",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_umidita_relativa_ambiente": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x01, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "humidity", "%", "Ambient Humidity",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_sonda_co2": (
# read      0:addres0000s, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x02, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "co2", "ppm", "Ambient CO2",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_temperatura_acqua": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x10, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Supply Water Temperature",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_temperatura_esterna": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x11, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Outdoor Temperature",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_stato_ventilatore_mandata": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x12, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", None, "%", "Supply Fan Status",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_stato_ventilatore_estrazione": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x13, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", None, "%", "Extractor Fan Status",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_set_temperatura_effettivo": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x14, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Actual Temperature Set",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_set_umidita_effettivo": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x15, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "humidity", "%", "Actual Humidity Set",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_set_ricambio_effettivo": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x16, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", None, None, "Actual Spare Set",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
        "ro_temperatura_mandata_aria": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x19, 1, CALL_TYPE_REGISTER_INPUT, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Air Supply Temperature",
# entity    10:manufacturer, 11:model
            "eneren", "rer_020i"),
    },
    Platform.SWITCH : {
        "device_power_control": (
# read      0:address, 1:function, 2:open, 3:close 
            0x00, CALL_TYPE_COIL, 0x01, 0x00,
# write     4:address, 5:function, 6:open, 7:close
            0x00, CALL_TYPE_WRITE_COILS, 0x01, 0x00,
# entity    8:default_label
            "Device Power",
# entity    9:manufacturer, 10:model            
            "eneren", "rer_020i"), 
    },
    Platform.NUMBER : {
        "operational_mode": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x01, 1, CALL_TYPE_COIL, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x01, CALL_TYPE_WRITE_COILS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 1, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Operational mode",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),

        "set_temperatura_ambiente_in_celsius": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x00, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x00, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            15, 30, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Set temperatura ambiente in celsius",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "set_umidità_relativa_ambiente": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x01, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x01, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            40, 90, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "humidity", "%", "Set umidità relativa ambiente",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "set_ricambio": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x02, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x02, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 5, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Set ricambio",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "temperatura_minima_invernale_senza_riscaldamento": (
#           Se l’aria di mandata èa una temperatura inferiore al valore impostato, la macchina attiverà la richiesta acqua
#           così da mitigare e non immettere aria troppo fredda.[se non presente controllo di temperatura di mandata modulante]
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0B, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x0B, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 90, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Temperatura minima invernale senza riscaldamento",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "temperatura_massima_estiva_senza_raffreddamento": (
#           Se l’aria di mandata è a una temperatura superiore al valore impostato, la macchina attiverà la richiesta
#           acqua così da mitigare e non immettere aria troppo calda.[se non presente controllo di temperatura di mandata modulante]
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0C, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x0C, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 90, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Temperatura massima estiva senza raffreddamento",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "gestione_raffreddamento": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0D, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x0D, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 2, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Gestione raffreddamento",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "protezione_dewpoint_differenziale": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0E, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x0E, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            -10, 10, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Protezione dew-point, differenziale",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "protezione_dewpoint_valore_t_dewpoint": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0F, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 0.1,
# write     6:address, 7:function, 8:scale
            0x0F, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            10, 40, 0.5, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            "measurement", "temperature", "°C", "Protezione dew-point, valore T dew-point",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
        "richiesta_attivazione_compressore": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x13, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 1,
# write     6:address, 7:function, 8:scale
            0x13, CALL_TYPE_WRITE_REGISTERS, 1,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 2, 1, "box",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, None, "Richiesta attivazione compressore",
# entity    17:manufacturer, 18:model
            "eneren", "rer_020i"),
    }
}

R4D3B16_REGISTERS = {
    #                       0       1        2           3                    4                 5                6        7         8                            9         10     
    #                   address, cmd open, cmd close, function,            address,          function,         st open, st close, label,                     manufacturer, model
    "relay_channel_01": (0x0001, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0001, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 1)", "eletechsup", "r4d3b16"),
    "relay_channel_02": (0x0002, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0002, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 2)", "eletechsup", "r4d3b16"),
    "relay_channel_03": (0x0003, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0003, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 3)", "eletechsup", "r4d3b16"),
    "relay_channel_04": (0x0004, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0004, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 4)", "eletechsup", "r4d3b16"),
    "relay_channel_05": (0x0005, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0005, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 5)", "eletechsup", "r4d3b16"),
    "relay_channel_06": (0x0006, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0006, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 6)", "eletechsup", "r4d3b16"),
    "relay_channel_07": (0x0007, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0007, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 7)", "eletechsup", "r4d3b16"),
    "relay_channel_08": (0x0008, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0008, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 8)", "eletechsup", "r4d3b16"),
    "relay_channel_09": (0x0009, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0009, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 9)", "eletechsup", "r4d3b16"),
    "relay_channel_10": (0x000A, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000A, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 10)", "eletechsup", "r4d3b16"),
    "relay_channel_11": (0x000B, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000B, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 11)", "eletechsup", "r4d3b16"),
    "relay_channel_12": (0x000C, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000C, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 12)", "eletechsup", "r4d3b16"),
    "relay_channel_13": (0x000D, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000D, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 13)", "eletechsup", "r4d3b16"),
    "relay_channel_14": (0x000E, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000E, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 14)", "eletechsup", "r4d3b16"),
    "relay_channel_15": (0x000F, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x000F, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 15)", "eletechsup", "r4d3b16"),
    "relay_channel_16": (0x0010, 0x0100, 0x0200, CALL_TYPE_WRITE_REGISTER, 0x0010, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000, "Relay Channel (Channel 16)", "eletechsup", "r4d3b16"),
    Platform.SWITCH : {
        "relay_channel_01": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0001, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0001, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 1)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_02": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0002, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0002, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 2)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_03": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0003, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0003, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 3)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_04": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0004, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0004, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 4)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_05": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0005, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0005, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 5)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_06": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0006, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0006, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 6)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_07": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0007, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0007, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 7)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_08": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0008, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0008, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 8)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_09": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0009, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0009, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 9)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_10": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000A, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000A, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 10)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_11": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000B, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000B, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 11)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_12": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000C, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000C, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 12)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_13": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000D, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000D, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 3)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_14": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000E, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000E, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 14)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_15": (
# read      0:address, 1:function, 2:open, 3:close 
            0x000F, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x000F, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 15)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
        "relay_channel_16": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0010, CALL_TYPE_REGISTER_HOLDING, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0010, CALL_TYPE_WRITE_REGISTER, 0x0100, 0x0200,
# entity    8:default_label
            "Relay Channel (Channel 6)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "r4d3b16"), 
    },
 }

E10IOA04_REGISTERS = {
    #                       0       1        2           3                    4                 5                6        7         8                            9         10     
    #                   address, cmd open, cmd close, function,            address,          function,         st open, st close, label,                     manufacturer, model
    "relay_channel_01": (0x0000, 0x0001, 0x0000, CALL_TYPE_WRITE_COIL, 0x0000, CALL_TYPE_COIL, 0x0001, 0x0000, "Relay Channel (Channel 1)", "eletechsup", "10ioa04"),
    "relay_channel_02": (0x0001, 0x0001, 0x0000, CALL_TYPE_WRITE_COIL, 0x0001, CALL_TYPE_COIL, 0x0001, 0x0000, "Relay Channel (Channel 2)", "eletechsup", "10ioa04"),
    "relay_channel_03": (0x0002, 0x0001, 0x0000, CALL_TYPE_WRITE_COIL, 0x0002, CALL_TYPE_COIL, 0x0001, 0x0000, "Relay Channel (Channel 3)", "eletechsup", "10ioa04"),
    "relay_channel_04": (0x0003, 0x0001, 0x0000, CALL_TYPE_WRITE_COIL, 0x0003, CALL_TYPE_COIL, 0x0001, 0x0000, "Relay Channel (Channel 4)", "eletechsup", "10ioa04"),
    Platform.SWITCH : {
        "relay_channel_01": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0000, CALL_TYPE_COIL, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0000, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 1)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "10ioa04"), 
        "relay_channel_02": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0001, CALL_TYPE_COIL, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0001, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 2)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "10ioa04"),     
        "relay_channel_03": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0002, CALL_TYPE_COIL, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0002, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 3)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "10ioa04"),   
        "relay_channel_04": (
# read      0:address, 1:function, 2:open, 3:close 
            0x0003, CALL_TYPE_COIL, 0x0001, 0x0000,
# write     4:address, 5:function, 6:open, 7:close
            0x0003, CALL_TYPE_WRITE_COIL, 0x0001, 0x0000,
# entity    8:default_label
            "Relay Channel (Channel 4)",
# entity    9:manufacturer, 10:model            
            "eletechsup", "10ioa04"),   
    },
 }


N4DBA06_REGISTERS = {
    #    0       1        2           3             4           5        6        7             8         9      10       11        12
    # address, count, function, src_datatype, tgt_datatype, precision, scale state class, device class, unit, label, manufacturer, model
    "vin1_value": (0x0000, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.01, "measurement", "voltage", "V", "Voltage in (Channel 1)", "eletechsup", "n4dba06"),
    "vin2_value": (0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.01, "measurement", "voltage", "V", "Voltage in (Channel 2)", "eletechsup", "n4dba06"),
    "vin2_value_percentage": (0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, int, 0, 0.1, None, None, "%", "Voltage in (Channel 2)", "eletechsup", "n4dba06"),

    "vin1_ratio": (0x0007, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 1)", "eletechsup", "n4dba06"),
    "vin2_ratio": (0x0008, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 2)", "eletechsup", "n4dba06"),

    "vout1_value": (0x0080, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 0.1, "measurement", "voltage", "V", "Voltage in (Channel 1)", "eletechsup", "n4dba06"),
    "vout2_value": (
        0x0081, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 0.1,
        0x0081, CALL_TYPE_WRITE_REGISTER, 10,
        0, 100, 1, "slider",
        None, None, "%", "Voltage out 2 (range 0 100)",
        "eletechsup", "n4dba06"),
    "vout1_ratio": (0x0087, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 1)", "eletechsup", "n4dba06"),
    "vout2_ratio": (0x0088, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 2)", "eletechsup", "n4dba06"),

    Platform.SENSOR : {
#       "vin1_value": (0x0000, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.01, "measurement", "voltage", "V", "Voltage in (Channel 1)", "eletechsup", "n4dba06"),
        "vin2_value": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.01,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "voltage", "V", "Voltage In (Channel 2)",
# entity    10:manufacturer, 11:model
            "eletechsup", "n4dba06"),
        "vin2_value_percentage": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 0, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            None, None, "%", "Voltage in (Channel 2)",
# entity    10:manufacturer, 11:model
            "eletechsup", "n4dba06"),
#       "vin1_ratio": (0x0007, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 1)", "eletechsup", "n4dba06"),
#       "vin2_ratio": (0x0008, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 2)", "eletechsup", "n4dba06"),
    },
    Platform.NUMBER : {
#       "vout1_value": (0x0080, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 0.1, "measurement", "voltage", "V", "Voltage in (Channel 1)", "eletechsup", "n4dba06"),
        "vout2_value": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0081, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 1, 10,
# write     6:address, 7:function, 8:scale
            0x0081, CALL_TYPE_WRITE_REGISTER, 10,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 100, 1, "slider",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, "%", "Voltage Out Percentage (Channel 2)",
# entity    17:manufacturer, 18:model
            "eletechsup", "n4dba06"),   
        "vout2_value_percentage": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0081, 1, CALL_TYPE_REGISTER_HOLDING, DataType.INT16, 0, 0.1,
# write     6:address, 7:function, 8:scale
            0x0081, CALL_TYPE_WRITE_REGISTER, 10,
# number    9:min, 10:max, 11:step, 12:mode (auto, box, slider)
            0, 100, 1, "slider",
# entity    13:state_class, 14:device_class, 15:unit_of_measurement, 16:default_label
            None, None, "%", "Voltage Out Percentage (Channel 2)",
# entity    17:manufacturer, 18:model
            "eletechsup", "n4dba06"),        
#       "vout1_ratio": (0x0087, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 1)", "eletechsup", "n4dba06"),
#       "vout2_ratio": (0x0088, 1, CALL_TYPE_WRITE_REGISTER, DataType.UINT16, float, 1, 1, "measurement", "battery", "%", "Ratio Voltage in (Channel 2)", "eletechsup", "n4dba06"),
    }
}

NT18B07_REGISTERS = {
    #    0       1        2           3             4           5        6        7             8         9      10       11        12
    # address, count, function, src_datatype, tgt_datatype, precision, scale state class, device class, unit, label, manufacturer, model
    "ch0_temperature": (0x0000, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 0)", "eletechsup", "nt18b07"),
    "ch1_temperature": (0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 1)", "eletechsup", "nt18b07"),
    "ch2_temperature": (0x0002, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 2)", "eletechsup", "nt18b07"),
    "ch3_temperature": (0x0003, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 3)", "eletechsup", "nt18b07"),
    "ch4_temperature": (0x0004, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 4)", "eletechsup", "nt18b07"),
    "ch5_temperature": (0x0005, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 5)", "eletechsup", "nt18b07"),
    "ch6_temperature": (0x0006, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, float, 1, 0.1, "measurement", "temperature", "°C", "Temperature (Channel 6)", "eletechsup", "nt18b07"),
    Platform.SENSOR : {
        "ch0_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0000, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 0)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch1_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0001, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 1)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch2_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0002, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 2)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch3_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0003, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 3)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch4_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0004, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 4)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch5_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0005, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 5)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
        "ch6_temperature": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0006, 1, CALL_TYPE_REGISTER_HOLDING, DataType.UINT16, 1, 0.1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "temperature", "°C", "Temperature (Channel 6)",
# entity    10:manufacturer, 11:model
            "eletechsup", "nt18b07"),
       
    }
}
SDM120M_REGISTERS = {
    #    0       1        2           3             4           5        6        7             8         9      10       11        12
    # address, count, function, src_datatype, tgt_datatype, precision, scale state class, device class, unit, label, manufacturer, model
    "voltage": (0x0000, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, 1, 1, "measurement", "voltage", "V", "Voltage", "Eastron", "sdm120m"),
    "current": (0x0006, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, 1,  1, "measurement", "current", "A", "Current", "Eastron", "sdm120m"),
    "power_active": (0x000c, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, 1, 1, "measurement", "power", "W", "Power (Active)", "Eastron", "sdm120m" ),
    # "power_apparent": (0x0012, 2,CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, "Power (Apparent)", "VA", 1, 1),    
    # "power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1, 1),
    # "power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power Factor", "", 1, 1),
    # "phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Phase Angle", "°", 1, 1),
    # "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
    # "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
    # "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
    # "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
    # "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
    # "total_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2, 1),
    # "maximum_total_demand_power_active": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2, 1),
    # "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
    # "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
    # "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
    # "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
    # "total_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Current", "A", 3, 1),
    # "maximum_total_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3, 1),
    "total_energy_active": (0x0156, 2,CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, 2, 1, "total", "energy", "kWh", "Total Energy (Active)", "Eastron", "sdm120m" ),
    # "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),
    # "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
    # "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
    # "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
    # "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
    #     "N-1", "E-1", "O-1", "N-2"], 1, 1),
    # "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
    # "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
    #     2400, 4800, 9600, -1, -1, 1200], 1, 1),
    # "p1_output_mode": (0x0056, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Output Mode", [
    #     0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
    #     "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2, 1),
    # "display_scroll_timing": (0xf900, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3, 1),
    # "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
    #     "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3, 1),
    # "measurement_mode": (0xf920, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Measurement Mode", [
    #     0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3, 1),
    # "indicator_mode": (0xf930, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
    #     "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"], 3, 1),
    # "serial_number": (0xfc00, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Serial Number", "", 4, 1),
    # "software_version": (0xfc03, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Software Version", "", 4, 1)

    Platform.SENSOR : {
        "voltage": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0000, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, 1, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "voltage", "V", "Voltage",
# entity    10:manufacturer, 11:model
            "eastron", "sdm120m"),
        "current": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0006, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, 1, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "current", "A", "Current",
# entity    10:manufacturer, 11:model
            "eastron", "sdm120m"),
        "power_active": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x000C, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, 1, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "measurement", "power", "W", "Power (Active)",
# entity    10:manufacturer, 11:model
            "eastron", "sdm120m"),
        # "power_apparent": (0x0012, 2,CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, float, "Power (Apparent)", "VA", 1, 1),    
        # "power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1, 1),
        # "power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power Factor", "", 1, 1),
        # "phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Phase Angle", "°", 1, 1),
        # "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
        # "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
        # "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
        # "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
        # "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
        # "total_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2, 1),
        # "maximum_total_demand_power_active": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2, 1),
        # "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
        # "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
        # "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
        # "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
        # "total_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Current", "A", 3, 1),
        # "maximum_total_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3, 1),
        "total_energy_active": (
# read      0:address, 1:quantity, 2:function, 3:data_type, 4:precision, 5:scale 
            0x0156, 2, CALL_TYPE_REGISTER_INPUT, DataType.FLOAT32, 2, 1,
# entity    6:state_class, 7:device_class, 8:unit_of_measurement, 9:default_label
            "total", "energy", "kWh", "Total Energy (Active)",
# entity    10:manufacturer, 11:model
            "eastron", "sdm120m"),
        # "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),
        # "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
        # "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
        # "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
        # "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
        #     "N-1", "E-1", "O-1", "N-2"], 1, 1),
        # "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
        # "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
        #     2400, 4800, 9600, -1, -1, 1200], 1, 1),
        # "p1_output_mode": (0x0056, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Output Mode", [
        #     0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
        #     "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2, 1),
        # "display_scroll_timing": (0xf900, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3, 1),
        # "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
        #     "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3, 1),
        # "measurement_mode": (0xf920, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Measurement Mode", [
        #     0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3, 1),
        # "indicator_mode": (0xf930, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
        #     "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"], 3, 1),
        # "serial_number": (0xfc00, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Serial Number", "", 4, 1),
        # "software_version": (0xfc03, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Software Version", "", 4, 1)

    }
}

BOARDS_AND_REGISTERS = {
    Board.AERMEC_HMI080: AERMEC_HMI080_REGISTERS,
    Board.EASTRON_SDM120M: SDM120M_REGISTERS,
    Board.ENEREN_RER020I_EFHR0_EVO: RER020I_EFHR0_EVO_REGISTERS,
    Board.ELETECHSUP_10IOA04: E10IOA04_REGISTERS,
    Board.ELETECHSUP_N4DBA06: N4DBA06_REGISTERS,
    Board.ELETECHSUP_NT18B07: NT18B07_REGISTERS,
    Board.ELETECHSUP_R4D3B16: R4D3B16_REGISTERS,
    Board.WAVESHARE_RTU_RELAY : WAVESHARE_RTU_RELAY_REGISTERS,
}

BOARD_SENSORS = {
    Board.EASTRON_SDM120M: SDM120M_REGISTERS,
    Board.ELETECHSUP_NT18B07: NT18B07_REGISTERS,
    Board.ELETECHSUP_N4DBA06: N4DBA06_REGISTERS,
    Board.ENEREN_RER020I_EFHR0_EVO: RER020I_EFHR0_EVO_REGISTERS,
}

BOARD_SWITCHES = {
    Board.ELETECHSUP_R4D3B16: R4D3B16_REGISTERS,
    Board.ELETECHSUP_10IOA04: E10IOA04_REGISTERS,
}
