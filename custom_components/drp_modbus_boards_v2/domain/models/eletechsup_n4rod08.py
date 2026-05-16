"""Module for ELETECHSUP N4ROD08 board registers."""
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
#   ELETECHSUP N4ROD08
####### ####### ####### ####### #######
@register_board(Board.ELETECHSUP_N4ROD08)
def _eletechsup_n4rod08_regs():
    return BoardDefinition(
        metadata=Metadata(
            name="8ch RS485 Modbus RTU Relay",
            manufacturer="eletechsup",
            model="n4rod08",
        ),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x0000,
                count=8,  # 8 relays, registers 0x0000–0x0007

                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTER,

                state_on=0x0001,    # FC03 read: relay is ON
                state_off=0x0000,   # FC03 read: relay is OFF
                command_on=0x0100,  # FC06 write: Open relay (turn ON load)
                command_off=0x0200, # FC06 write: Close relay (turn OFF load)
            )
        },
        registers={
            Platform.SWITCH: Register(
                functions={
                    # Per doc: channel N is at register address 0x0000 + (N-1)
                    # i.e. channel 1 → 0x0000, channel 2 → 0x0001, ... channel 8 → 0x0007
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
                    SwitchFunction.CHANNEL_04: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0004,
                    ),
                    SwitchFunction.CHANNEL_05: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0005,
                    ),
                    SwitchFunction.CHANNEL_06: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0006,
                    ),
                    SwitchFunction.CHANNEL_07: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0007,
                    ),
                }
            )
        },
    )