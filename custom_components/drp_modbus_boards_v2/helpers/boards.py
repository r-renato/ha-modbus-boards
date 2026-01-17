"""Boards registry for drp_modbus_boards_v2 integration."""
from __future__ import annotations

from typing import Any, Callable, Dict, TYPE_CHECKING, Union
import logging

from pymodbus.pdu.pdu import ModbusPDU

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    Platform,
)
from homeassistant.components.modbus.const import (
    DataType,
)

from ..helpers.logger import log_debug

from ..helpers.modbus import decode_registers_2_value
from ..const import DEVICE_AREAS_DATA, DOMAIN

from ..helpers.utils import slugify

from ..domain.boards import ModbusRegistersResponse, RegisterArea, RegisterFunction
from ..domain.enums import Board, RegisterAreaName

if TYPE_CHECKING:
    # Import solo per i type checker, evita cicli di import a runtime
    from ..domain.boards import BoardDefinition

BoardKey = Union[Board, str]
BoardFactory = Callable[[], "BoardDefinition"]

# registry: chiave normalizzata -> factory che crea un BoardDefinition
_REGISTRY: Dict[str, BoardFactory] = {}

_LOGGER = logging.getLogger(__name__)

def _normalize_board_key(board: BoardKey) -> str:
    """Normalizza la chiave della board in una stringa.

    - Se è un Enum Board -> usa board.value (es. 'eletechsup_r4d3b16')
    - Se è già una stringa -> la converte in str() (difensivo)
    """
    if isinstance(board, Board):
        return board.value
    return str(board)


def register_board(board: BoardKey):
    """Decorator per registrare una board con una factory lazy dei BoardDefinition."""

    key = _normalize_board_key(board)

    def _wrap(factory: BoardFactory) -> BoardFactory:
        _REGISTRY[key] = factory
        return factory

    return _wrap

def get_boards() -> dict[str, "BoardDefinition"]:
    """Istanzia tutte le boards (BoardDefinition), on-demand."""
    return {b: f() for b, f in _REGISTRY.items()}


def get_board_definition(board: BoardKey) -> "BoardDefinition":
    """Istanzia e restituisce il BoardDefinition richiesto, on-demand."""
    key = _normalize_board_key(board)
    try:
        factory = _REGISTRY[key]
    except KeyError as exc:
        # piccolo aiuto di debug: mostra le chiavi registrate
        available = ", ".join(_REGISTRY.keys()) or "<vuoto>"
        raise ValueError(
            f"Board non registrata: {key!r}. Registry contiene: {available}"
        ) from exc

    return factory()

def get_board_register_function(
    board: BoardKey,
    platform: Platform,
    device_function: str,
) -> RegisterFunction | None:
    """..."""
    _board_def: BoardDefinition = get_board_definition(board)
    _functions = _board_def.registers[platform].functions

    return _functions.get(device_function)

def gen_board_data_area_key(board: Union[Board, str], slave: int, area_name: Union[RegisterAreaName, str]) -> str:
    return slugify(f"{board}-{slave}-{area_name}")

def store_board_data_area(
        hass: HomeAssistant,
        data: Any, 
        key: str
) -> None:
    storage = hass.data.setdefault(DOMAIN, {}).setdefault(DEVICE_AREAS_DATA, {})

    stored_response: ModbusRegistersResponse | None = storage.get(key)

    if stored_response is None:
        storage[key] = ModbusRegistersResponse(registers_response=data)
    else:
        stored_response.update_response(registers_response=data)

def get_stored_board_data_area(
        hass: HomeAssistant,
        key: str
) -> ModbusRegistersResponse:
    storage = hass.data.setdefault(DOMAIN, {}).setdefault(DEVICE_AREAS_DATA, {})
    
    return storage.get(key)

    
def get_value_from_modbus_response(
    modbus_response: ModbusPDU,
    address: int,
    datatype: DataType
) -> Any:
    """Estrae il valore relativo a `address` da una risposta Modbus.

    La risposta contiene un intero set di registri/coil; `address` è l'offset
    all'interno di quel set (0-based).

    Usa il NOME DELLA CLASSE della risposta per distinguere il tipo:
    - ReadHoldingRegistersResponse / ReadInputRegistersResponse -> registers
    - ReadCoilsResponse / ReadDiscreteInputsResponse           -> bits
    """

    if address < 0:
        raise ValueError(f"Address deve essere >= 0 (address={address})")

    class_name = type(modbus_response).__name__

    # Mappatura tra nome classe e tipo di payload
    registers_classes = {
        "ReadHoldingRegistersResponse",
        "ReadInputRegistersResponse",
    }
    bits_classes = {
        "ReadCoilsResponse",
        "ReadDiscreteInputsResponse",
    }

    # Registri (16-bit)
    if class_name in registers_classes:
        registers = getattr(modbus_response, "registers", None) or []
        try:
            return decode_registers_2_value(registers=registers, index=address, data_type=datatype)
            # return registers[address]
        except IndexError as err:
            raise IndexError(
                f"Address {address} fuori range per {class_name} (len(registers)={len(registers)})"
            ) from err

    # Coil / Discrete (bit/boolean)
    if class_name in bits_classes:
        bits = getattr(modbus_response, "bits", None) or []
        try:
            return bits[address]
        except IndexError as err:
            raise IndexError(
                f"Address {address} fuori range per {class_name} (len(bits)={len(bits)})"
            ) from err

    # Tipo di risposta non riconosciuto
    raise TypeError(
        f"Tipo di risposta Modbus non supportato per l'estrazione del valore: {class_name!r}"
    )

def transform_from_modbus_raw_value(
    raw_value: Any,
    offset_value: float,
    register_area: RegisterArea,
    register_function: RegisterFunction,        
    platform: Platform,
) -> bool | int | float | str:
    """..."""

    fr = register_function.function_read
    
    if platform in (Platform.NUMBER, Platform.SENSOR):
        scale: float | None = fr.scale if fr is not None else None
        precision: float | None = fr.precision if fr is not None else None
        
        min_value: int | None = register_function.min
        max_value: int | None = register_function.max

        default_value: int | None = register_function.default

        try:
            value = float(raw_value)
        except Exception as err:  # noqa: BLE001
            # Se non è numerico, non possiamo procedere
            msg = (
                f"Error transforming Modbus raw value: '{raw_value}' "
                f"{err}"
            )
            return msg
    
        if scale is not None and scale != 1:
            value = value * scale

        # aggiungo l'eventuale offset
        value = value + offset_value

        if default_value is None or (default_value is not None and value != default_value):
            if (min_value is not None and value < min_value):
                msg = (
                    f"Error transforming Modbus raw value: '{raw_value}' "
                    f"[scale={scale}, min value={min_value}, max value={max_value}] value={value} < min value"
                )
                return msg
            
            if (max_value is not None and value > max_value):
                msg = (
                    f"Error transforming Modbus raw value: '{raw_value}' "
                    f"[scale={scale}, min value={min_value}, max value={max_value}] value={value} > max value"
                )
                return msg

        if precision is not None:
            value = round(float(value), precision)
            if precision == 0:
                return int(value)

        return value

    elif platform in (Platform.SWITCH, Platform.BINARY_SENSOR):
        state_on = register_area.state_on
        state_off = register_area.state_off

        if fr is not None and fr.state_on is not None:
            state_on = fr.state_on

        if fr is not None and fr.state_off is not None:
            state_off = fr.state_off

        state_on = state_on if state_on is not None else True
        state_off = state_off if state_off is not None else False

        if raw_value == state_on:
            return True
        elif raw_value == state_off:
            return False
        else:
            msg = (
                f"Error transforming Modbus raw value: '{raw_value}' {type(raw_value)} != [{state_on} or {state_off}]"
                f"[area state on={register_area.state_on}, area state off={register_area.state_off}, "
                f"fr state on={fr.state_on if fr is not None else None}, fr state off={fr.state_off if fr is not None else None}]"
            )
            return msg
    else:
        msg = (
            f"Error transforming Modbus raw value: '{raw_value}', unsupported platform={platform}"
        )
        return msg

def apply_register_read_transform(
    raw_value: Any,
    offset: float,
    register_function: RegisterFunction | None,
) -> Any:
    """Applica scale, precision, min e max al valore grezzo.

    Usa le definizioni in RegisterFunction.function_read e RegisterFunction.
    """

    if register_function is None:
        return raw_value

    value = raw_value
    fr = register_function.function_read

    # 1) scale (es. 0.1 per convertirlo in °C, kW, ecc.)
    scale: float | None = fr.scale if fr is not None else None
    if scale is not None:
        try:
            value = float(value) * scale
        except Exception:  # noqa: BLE001
            # Se non è convertibile, lascio il valore grezzo
            return raw_value

    # 2) validazione min/max (NON clamp)
    min_v = register_function.min
    max_v = register_function.max

    try:
        num = float(value)
    except Exception:  # noqa: BLE001
        # Se non è numerico, non possiamo confrontare -> lasciamo raw_value
        return raw_value

    # Se è fuori dal range definito, consideriamo il valore non valido e
    # restituiamo direttamente il raw_value (senza ulteriori trasformazioni)
    if min_v is not None and num < min_v:
        return None
    if max_v is not None and num > max_v:
        return None

    # Se è dentro al range, lavoriamo con il numero validato
    value = num + offset

    # 3) precision (numero di decimali)
    precision: int | None = fr.precision if fr is not None else None
    if precision is not None:
        try:
            value = round(float(value), precision)
        except Exception:  # noqa: BLE001
            # mantieni il valore così com'è se non è numerico
            pass

    # log_debug(
    #         _LOGGER,
    #         "raw='%s' offset='%s' scale='%s' value='%s'",
    #         raw_value,
    #         offset,
    #         scale,
    #         value,
    # )
    return value

def get_board(board_str: str) -> Board:
    """
    Restituisce la Board corrispondente alla stringa passata.

    Accetta sia:
    - il valore della enum (es. "xy_mod01_sht20")
    - il nome della enum (es. "XY_MOD01_SHT20", case-insensitive)

    Solleva ValueError se la board non esiste.
    """
    # Prova prima a interpretare la stringa come value
    try:
        return Board(board_str)
    except ValueError:
        pass

    # Prova poi a interpretarla come name (case-insensitive)
    name = board_str.upper()
    try:
        return Board[name]
    except KeyError as exc:
        raise ValueError(f"Board sconosciuta: {board_str!r}") from exc











