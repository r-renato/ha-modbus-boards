"""Module for Eastron SDM120M board registers definition."""
from __future__ import annotations

from homeassistant.const import (
    ATTR_VOLTAGE,
    Platform,
    UnitOfEnergy,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
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
#   EASTRON SDM120M
####### ####### ####### ####### #######

@register_board(Board.EASTRON_SDM120M)
def _sdm120m_regs():
    return BoardDefinition(
        metadata = Metadata(name="Modbus Energy Meter", manufacturer="eastron", model="sdm120m"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=32,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.FLOAT32,
            ),
            RegisterAreaName.AREA_B: RegisterArea(
                address=0x0156,
                count=2,
                
                mdb_read_function=CALL_TYPE_REGISTER_INPUT,
                data_type=DataType.FLOAT32,
            )
        },
        registers = {
            Platform.SENSOR: Register(
                functions={
                    SensorFunction.VOLTAGE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x00,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class=ATTR_VOLTAGE,
                        unit_of_measurement=UnitOfElectricPotential.VOLT
                    ),
                    SensorFunction.CURRENT: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x06,

                        function_read=RegisterFunctionRead(
                            precision=2,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="current",
                        unit_of_measurement=UnitOfElectricCurrent.AMPERE
                    ),
                    SensorFunction.ACTIVE_POWER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0C,

                        function_read=RegisterFunctionRead(
                            precision=1,
                            scale=1,
                        ),

                        state_class="measurement",
                        device_class="power",
                        unit_of_measurement=UnitOfPower.WATT
                    ),
                    SensorFunction.TOTAL_ACTIVE_ENERGY: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x00,

                        function_read=RegisterFunctionRead(
                            precision=2,
                            scale=1,
                        ),

                        state_class="total",
                        device_class="energy",
                        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR
                    ),
                }
            )
        }
    )
