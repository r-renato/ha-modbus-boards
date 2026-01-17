"""Module for EletechSUP 10IOA04 board registers definition."""
from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_COIL,
    CALL_TYPE_WRITE_COIL,
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
#   ELETECHSUP 10IOA04
####### ####### ####### ####### #######

@register_board(Board.ELETECHSUP_10IOA04)
def _eletechsup_10ioa04_regs():
    return BoardDefinition(
        metadata = Metadata(name="4-ch DI-DO PLC IO RS485 Relay Switch", manufacturer="eletechsup", model="10ioa04"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=4,
                
                mdb_read_function=CALL_TYPE_COIL,
                mdb_write_function=CALL_TYPE_WRITE_COIL,

                state_on=True,  # relay state close
                state_off=False, # relay state open

                command_on=0xFF00,  # Relay state close
                command_off=0x0000, # Relay state open
            )
        },
        registers = {
            Platform.SWITCH: Register(
                functions={
                    SwitchFunction.CHANNEL_00: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0000,
                    ),
                    SwitchFunction.CHANNEL_01: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0001,
                    ),
                    SwitchFunction.CHANNEL_02: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0002,
                    ),
                    SwitchFunction.CHANNEL_03: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0003,
                    ),
                }
            )                

        }
    )
