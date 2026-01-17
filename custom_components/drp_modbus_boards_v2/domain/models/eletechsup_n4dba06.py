"""Module for ELETECHSUP N4DBA06 board registers."""
from __future__ import annotations

from homeassistant.const import (
    ATTR_VOLTAGE,
    PERCENTAGE,
    Platform,
    UnitOfElectricPotential,
)
from homeassistant.components.number import NumberMode
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_WRITE_REGISTER,
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
    RegisterFunctionRead,
    RegisterFunction,
    RegisterFunctionWrite,
)
from ..enums import Board, NumberFunction, RegisterAreaName, SensorFunction

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   ELETECHSUP N4DBA06
####### ####### ####### ####### #######

@register_board(Board.ELETECHSUP_N4DBA06)
def _eletechsup_n4dba06_regs():
    return BoardDefinition(
        metadata = Metadata(name="8-ch Analog Digital ADC DAC IO module", manufacturer="eletechsup", model="n4dba06"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=4,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                data_type=DataType.UINT16,
            ),
            RegisterAreaName.AREA_B: RegisterArea(
                address=0x0080,
                count=4,
                registry_area_shift=-0x80,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTER,
                data_type=DataType.UINT16,
            )
        },
        registers = {
            Platform.SENSOR: Register(
                functions={
                    SensorFunction.VOLTAGE_IN2: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x01,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.01,
                        ),

                        min=0,
                        max=11,

                        state_class="measurement",
                        device_class=ATTR_VOLTAGE,
                        unit_of_measurement=UnitOfElectricPotential.VOLT
                    ),
                    SensorFunction.VOLTAGE_IN2_PERCENTAGE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x01,

                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=0.1,
                        ),
                        
                        min=0,
                        max=100,

                        unit_of_measurement=PERCENTAGE
                    )
                }
            ),
            Platform.NUMBER: Register(
                functions={
                    NumberFunction.VOLTAGE_OUT2: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0081,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=0.5,
                            number_mode=NumberMode.BOX
                        ),
                        
                        min=0,
                        max=10,

                        state_class="measurement",
                        device_class=ATTR_VOLTAGE,
                        unit_of_measurement=UnitOfElectricPotential.VOLT
                    ),
                    NumberFunction.VOLTAGE_OUT2_PERCENTAGE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0081,
                        
                        function_read=RegisterFunctionRead(
                            precision=0,
                            scale=0.1,
                        ),
                        function_write=RegisterFunctionWrite(
                            scale=10,
                            step=1,
                            number_mode=NumberMode.BOX
                        ),

                        min=0,
                        max=100,

                        unit_of_measurement=PERCENTAGE
                    ),
                }
            )
        }
    )