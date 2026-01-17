"""Module for GauseLink GL-TH02-PE board registers definition."""
from __future__ import annotations

from homeassistant.const import (
    ATTR_TEMPERATURE,
    PERCENTAGE,
    Platform,
    UnitOfTemperature,
)
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_INPUT,
    DataType,
)

from ...helpers.boards import register_board
from ...helpers.ha import ensure_number_in_platforms
from ...const import CONF_NUMBERS
from ..boards import BoardDefinition, Metadata, Register, RegisterArea, RegisterFunction, RegisterFunctionRead
from ..enums import Board, RegisterAreaName, SensorFunction

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   XY MOD01 SHT20
####### ####### ####### ####### #######

@register_board(Board.GL_TH02_PE)
def _gl_th02_pe_regs():
    return BoardDefinition(
        metadata = Metadata(name="Modbus Temperature Humidity Outdoor Sensor", manufacturer="gauselink", model="gl-th02-pe"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=2,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.UINT16,
            )
        },
        registers = {
            Platform.SENSOR: Register(
                functions={
                    SensorFunction.TEMPERATURE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x01,

                        function_read=RegisterFunctionRead(precision=1,scale=0.1),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.HUMIDITY: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x00,

                        function_read=RegisterFunctionRead(precision=1,scale=0.1),

                        state_class="measurement",
                        device_class="humidity",
                        unit_of_measurement=PERCENTAGE
                    )
                }
            )
        }
    )
