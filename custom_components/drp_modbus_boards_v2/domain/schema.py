"""Schema for DRP Modbus Boards integration."""
from __future__ import annotations

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.sensor.const import (
    CONF_STATE_CLASS,
    DEVICE_CLASSES_SCHEMA as SENSOR_DEVICE_CLASSES_SCHEMA,
    STATE_CLASSES_SCHEMA as SENSOR_STATE_CLASSES_SCHEMA,
)
from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES_SCHEMA as BINARY_SENSOR_DEVICE_CLASSES_SCHEMA,
)
from homeassistant.components.switch import (
    DEVICE_CLASSES_SCHEMA as SWITCH_DEVICE_CLASSES_SCHEMA,
)
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.modbus.const import (
    CONF_ZERO_SUPPRESS,
    CONF_MIN_VALUE,
    CONF_MAX_VALUE,
    CONF_MSG_WAIT,
    CONF_NAN_VALUE,
    TCP,
    UDP,
    RTUOVERTCP,
)
from homeassistant.const import (
    CONF_SLAVE,
    CONF_BINARY_SENSORS,
    CONF_DEVICE_CLASS,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_OFFSET,
    CONF_SENSORS,
    CONF_SWITCHES,
    CONF_TYPE,
    CONF_TIMEOUT,
    CONF_DELAY,
    CONF_SCAN_INTERVAL,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ICON,
    CONF_MODE,
)

from .enums import Board

from ..const import (
    CONF_BOARD,
    CONF_DEVICE_FUNCTION,
    CONF_DEVICES,
    CONF_ENTITY_CONSTRAINT,
    CONF_NUMBERS,
    CONF_REVERSE,
    CONF_USED_ENTITY,
    DEFAULT_HUB,
    DOMAIN,
    MODE_AUTO,
    MODE_BOX,
    MODE_SLIDER,
)
from ..helpers.validators import (
    duplicate_entity_validator, 
    # duplicate_fan_mode_validator, 
    nan_validator, 
    number_validator, 
    scan_interval_validator, 
    # struct_validator
)
NUMBER_DEVICE_CLASSES_SCHEMA = vol.All(vol.Lower, vol.Coerce(NumberDeviceClass))

BASE_COMPONENT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Required(CONF_DEVICE_FUNCTION): cv.string,

        vol.Optional(CONF_USED_ENTITY, default=True): cv.boolean,
    }
)

SENSOR_SCHEMA = BASE_COMPONENT_SCHEMA.extend(
    {
        vol.Optional(CONF_OFFSET, default=0): number_validator,
        vol.Optional(CONF_MIN_VALUE): number_validator,
        vol.Optional(CONF_MAX_VALUE): number_validator,
        vol.Optional(CONF_NAN_VALUE): nan_validator,
        vol.Optional(CONF_ZERO_SUPPRESS): number_validator,

        vol.Optional(CONF_DEVICE_CLASS): SENSOR_DEVICE_CLASSES_SCHEMA,
        vol.Optional(CONF_STATE_CLASS): SENSOR_STATE_CLASSES_SCHEMA,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    }
)

BINARY_SENSOR_SCHEMA = BASE_COMPONENT_SCHEMA.extend(
    {
        vol.Optional(CONF_DEVICE_CLASS): BINARY_SENSOR_DEVICE_CLASSES_SCHEMA,
    }
)

SWITCH_SCHEMA = BASE_COMPONENT_SCHEMA.extend(
    {
        vol.Optional(CONF_REVERSE, default=False): cv.boolean,
        vol.Optional(CONF_DEVICE_CLASS): SWITCH_DEVICE_CLASSES_SCHEMA,
    }
)

NUMBER_SCHEMA = BASE_COMPONENT_SCHEMA.extend(
    {
        vol.Optional(CONF_ICON): cv.icon,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_MODE, default=MODE_SLIDER): vol.In([MODE_AUTO, MODE_BOX, MODE_SLIDER]),
        
        vol.Optional(CONF_DEVICE_CLASS): NUMBER_DEVICE_CLASSES_SCHEMA,
    }
)

MODBUS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_HUB): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=30): cv.positive_int,

        ### Modbus connection parameters for HA Modbus integration
        ### Do not remove these entry block!
        vol.Optional(CONF_TIMEOUT, default=3): cv.socket_timeout,
        vol.Optional(CONF_DELAY, default=0): cv.positive_int,
        vol.Optional(CONF_MSG_WAIT): cv.positive_int,
        ### Do not remove these entry block!

        vol.Optional(CONF_DEVICES): vol.All(cv.ensure_list, [
            vol.Schema({
                vol.Required(CONF_BOARD): vol.In(
                    [
                        Board.AERMEC_HMI080,
                        Board.EASTRON_SDM120M,
                        Board.ENEREN_RER020I_EFHR0_EVO,
                        Board.ELETECHSUP_10IOA04,
                        Board.ELETECHSUP_N4DBA06,
                        Board.ELETECHSUP_NT18B07,
                        Board.ELETECHSUP_R4D3B16,
                        Board.WAVESHARE_RTU_RELAY,
                        Board.XY_MOD01_SHT20,
                        Board.GL_TH02_PE,
                    ]
                ),
                vol.Required(CONF_SLAVE): cv.positive_int,
                vol.Required(CONF_NAME): cv.string,
                vol.Optional(CONF_ENTITY_CONSTRAINT): cv.string,

                vol.Optional(CONF_SENSORS): vol.All(cv.ensure_list, [vol.All(SENSOR_SCHEMA)]),
                vol.Optional(CONF_BINARY_SENSORS): vol.All(cv.ensure_list, [vol.All(BINARY_SENSOR_SCHEMA)]),
                vol.Optional(CONF_SWITCHES): vol.All(cv.ensure_list, [SWITCH_SCHEMA]),
                vol.Optional(CONF_NUMBERS): vol.All(cv.ensure_list, [NUMBER_SCHEMA]),
            })
        ]),
    }
)

ETHERNET_SCHEMA = MODBUS_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Required(CONF_TYPE): vol.Any(TCP, UDP, RTUOVERTCP),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            scan_interval_validator,
            duplicate_entity_validator,
            # duplicate_modbus_validator,
            [
                vol.Any(ETHERNET_SCHEMA),
            ],
        ),
    },
    extra=vol.ALLOW_EXTRA,
)
