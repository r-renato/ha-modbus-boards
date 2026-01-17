"""Module for Waveshare RTU Relay Modbus Board definitions."""
from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_COIL,
    CALL_TYPE_WRITE_COIL,
    CALL_TYPE_REGISTER_HOLDING,
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
#   Waveshare RTU Relay
####### ####### ####### ####### #######

@register_board(Board.WAVESHARE_RTU_RELAY)
def _waveshare_modbus_rtu_relay_regs():
    return BoardDefinition(
        metadata = Metadata(name="8ch Modbus relay module", manufacturer="waveshare", model="modbus_rtu_relay"),
        areas={
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x00FF,
                count=1,
                
                mdb_read_function=CALL_TYPE_COIL,
                mdb_write_function=CALL_TYPE_WRITE_COIL,

                state_on=0x0001, # relay state close
                state_off=0x0000, # relay state open

                command_on=0xFF00, # Relay state close
                command_off=0x0000, # Relay state open
            ),
            # RegisterAreaName.AREA_B: RegisterArea(
            #     address=0x2000,
            #     count=1,

            #     mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
            # )
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
        }
    )
