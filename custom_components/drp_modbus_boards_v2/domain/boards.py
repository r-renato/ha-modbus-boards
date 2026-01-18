"""... Boards domains data for drp_modbus_boards_v2 integration."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Union

from homeassistant.const import (
    Platform,
)
from homeassistant.components.number import NumberMode
from homeassistant.components.modbus.const import (
    DataType,
)

from .enums import RegisterAreaName

@dataclass
class Metadata:
    """Metadata for a Modbus board."""
    name: str
    manufacturer: str
    model: str

@dataclass
class RegisterArea:
    """Modbus register area definition."""
    address: int                             # Start address in board registries area
    count: int                               # Number of registers to read
    mdb_read_function: str                   # Modbus function code for reading
    mdb_write_function: Optional[str] = None # Modbus function code for writing
    data_type: Optional[DataType] = None     # Data type of the registers area
    registry_length: Optional[int] = None    # Length of each registry in the area

    registry_area_shift: int = 0   # Shift to apply to addresses in this area

    state_on: Optional[int] = None
    state_off: Optional[int] = None

    command_on: Optional[int] = None
    command_off: Optional[int] = None  

@dataclass
class RegisterFunctionBase:
    """Base class for Modbus register function definition."""
    scale: Optional[float] = 1

@dataclass
class RegisterFunctionRead(RegisterFunctionBase):
    """Modbus register read function definition."""
    precision: Optional[int] = 0

    state_on: Optional[int] = None
    state_off: Optional[int] = None


@dataclass
class RegisterFunctionWrite(RegisterFunctionBase):
    """Modbus register write function definition."""
    step: Optional[float] = None
    number_mode: NumberMode = NumberMode.AUTO

    command_on: Optional[int] = None
    command_off: Optional[int] = None  

@dataclass
class RegisterFunction:
    area: RegisterAreaName # Register area name

    address: int
    count: Optional[int] = None
    data_type: Optional[DataType] = None    # Data type of the registers area

    function_read: Optional[RegisterFunctionRead] = None
    function_write: Optional[RegisterFunctionWrite] = None

    min: Optional[float] = None
    max: Optional[float] = None
    default: Optional[int] = None

    state_class: Optional[str] = None
    device_class: Optional[str] = None
    unit_of_measurement: Optional[str] = None

    description: Optional[str] = None

@dataclass
class Register:
    """Modbus registries block definition."""
    functions: dict[str, RegisterFunction]

@dataclass
class BoardDefinition:
    metadata: Metadata
    areas: Dict[Union[RegisterAreaName, str], RegisterArea]
    registers: Dict[Platform, Register]

    def get_register(self, platform: Platform) -> Register | None:
        """Restituisce il Register per una piattaforma, se presente."""
        return self.registers.get(platform)

    # # opzionale: se vuoi mantenere la compatibilità con la vecchia struttura dict
    # def as_mapping(self) -> dict:
    #     """Ritorna una view tipo dict come quella che avevi prima."""
    #     data: dict = {METADATA: self.metadata}
    #     data.update(self.registers)
    #     return data

    # def __getitem__(self, key):
    #     """Permette board_def[METADATA] e board_def[Platform.SWITCH]."""
    #     if key is METADATA:
    #         return self.metadata
    #     if isinstance(key, Platform):
    #         return self.registers[key]
    #     raise KeyError(key)


@dataclass
class ModbusRegistersResponse:
    registers_response: Any
    error_count: int = 0
    last_response: datetime = field(default_factory=datetime.now)
    last_error: Optional[datetime] = None

    def update_response(self, registers_response: Any) -> None:
        """Aggiorna la risposta Modbus e, se presente, registra un errore."""

        if registers_response is None:
            return
        
        self.registers_response = registers_response
        self.last_response = datetime.now()

        if registers_response.status == 0:
            self.error_count += 1
            self.last_error = datetime.now()

    






