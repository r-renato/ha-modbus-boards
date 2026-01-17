"""Module for ELETECHSUP NT18B07 board definition."""
from __future__ import annotations

from homeassistant.const import (
    ATTR_TEMPERATURE,
    Platform,
    UnitOfTemperature,
)
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    DataType,
)

from ...helpers.boards import register_board
from ...helpers.ha import ensure_number_in_platforms
from ...const import CONF_NUMBERS
from ..boards import (
    BoardDefinition,
    Metadata,
    Register,
    RegisterArea,
    RegisterFunction,
    RegisterFunctionRead,
)
from ..enums import Board, RegisterAreaName, SensorFunction

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   ELETECHSUP NT18B07
####### ####### ####### ####### #######

@register_board(Board.ELETECHSUP_NT18B07)
def _eletechsup_nt18b07_regs():
    return BoardDefinition(
        metadata = Metadata(name="7-ch RS485 NTC Temperature Sensor", manufacturer="eletechsup", model="nt18b07"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=7,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                data_type=DataType.UINT16,
            )
        },
        registers = {
            Platform.SENSOR: Register(
                functions={
                    SensorFunction.CHANNEL_00: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x00,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_01: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x01,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_02: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x02,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_03: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x03,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_04: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x04,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_05: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x05,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                    SensorFunction.CHANNEL_06: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x06,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),

                        min=-10,
                        max=90,

                        state_class="measurement",
                        device_class=ATTR_TEMPERATURE,
                        unit_of_measurement=UnitOfTemperature.CELSIUS
                    ),
                }
            )
        }
    )