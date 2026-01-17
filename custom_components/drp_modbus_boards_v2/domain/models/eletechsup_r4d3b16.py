"""Module for ELETECHSUP R4D3B16 board registers."""
from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_WRITE_REGISTER,
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
)
from ..enums import Board, RegisterAreaName, SwitchFunction

# crea una nuova tupla aggiungendo la tua voce
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   ELETECHSUP R4D3B16
####### ####### ####### ####### #######

@register_board(Board.ELETECHSUP_R4D3B16)
def _eletechsup_r4d3b16_regs():
    return BoardDefinition(
        metadata = Metadata(name="16ch RS485 Modbus RTU Relay", manufacturer="eletechsup", model="r4d3b16"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0001,
                count=16,
                registry_area_shift=-1, # Area A starts at address 1, so we shift by -1 to map to 0-based indexing
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTER,
                
                state_on=0x0001,  # relay state close (on)
                state_off=0x0000, # relay state open (off)

                command_on=0x0100,   # Relay command close (256)
                command_off=0x0200,  # Relay command open (512)
            )
        },
        registers = {
            Platform.SWITCH: Register(
                functions={
                    SwitchFunction.CHANNEL_00: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0001,
                    ),
                    SwitchFunction.CHANNEL_01: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0002,
                    ),
                    SwitchFunction.CHANNEL_02: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0003,
                    ),
                    SwitchFunction.CHANNEL_03: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0004,
                    ),
                    SwitchFunction.CHANNEL_04: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0005,
                    ),
                    SwitchFunction.CHANNEL_05: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0006,
                    ),
                    SwitchFunction.CHANNEL_06: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0007,
                    ),
                    SwitchFunction.CHANNEL_07: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0008,
                    ),
                    SwitchFunction.CHANNEL_08: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0009,
                    ),
                    SwitchFunction.CHANNEL_09: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000A,
                    ),
                    SwitchFunction.CHANNEL_10: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000B,
                    ),
                    SwitchFunction.CHANNEL_11: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000C,
                    ),
                    SwitchFunction.CHANNEL_12: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000D,
                    ),
                    SwitchFunction.CHANNEL_13: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000E,
                    ),
                    SwitchFunction.CHANNEL_14: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x000F,
                    ),
                    SwitchFunction.CHANNEL_15: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0010, #16
                    ),
                }
            )                

        }
    )
    