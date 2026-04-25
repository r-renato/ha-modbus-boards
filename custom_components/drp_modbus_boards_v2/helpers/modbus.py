from __future__ import annotations

import asyncio
import itertools
import logging
import struct
from enum import StrEnum
from typing import Any, Sequence, Union, Iterable, List, Literal, TypeAlias, overload, TypeGuard
from weakref import WeakKeyDictionary

from homeassistant.components.modbus.modbus import ModbusHub
from homeassistant.components.modbus.const import DataType

from ..domain.boards import Register, RegisterArea, RegisterFunction

_LOGGER = logging.getLogger(__name__)

_PRIORITY_WRITE = 0
_PRIORITY_READ = 10


class _ModbusRequestQueue:
    def __init__(self, modbus_hub: ModbusHub) -> None:
        self._modbus_hub = modbus_hub
        self._queue: asyncio.PriorityQueue[
            tuple[int, int, dict[str, Any], asyncio.Future[Any]]
        ] = asyncio.PriorityQueue()
        self._counter = itertools.count()
        self._task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while True:
            priority, _, call_kwargs, future = await self._queue.get()
            try:
                result = await self._modbus_hub.async_pb_call(**call_kwargs)
                if not future.cancelled():
                    future.set_result(result)
            except Exception as err:  # noqa: BLE001
                if not future.cancelled():
                    future.set_exception(err)
            finally:
                self._queue.task_done()

    async def enqueue(self, priority: int, call_kwargs: dict[str, Any]) -> Any:
        future: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        await self._queue.put((priority, next(self._counter), call_kwargs, future))
        return await future


_QUEUE_BY_HUB: WeakKeyDictionary[ModbusHub, _ModbusRequestQueue] = WeakKeyDictionary()


def _get_queue(modbus_hub: ModbusHub) -> _ModbusRequestQueue:
    queue = _QUEUE_BY_HUB.get(modbus_hub)
    if queue is None:
        queue = _ModbusRequestQueue(modbus_hub)
        _QUEUE_BY_HUB[modbus_hub] = queue
    return queue


async def _enqueue_modbus_call(
    modbus_hub: ModbusHub,
    *,
    priority: int,
    unit: int,
    address: int,
    value: int,
    use_call: str,
) -> Any:
    call_kwargs = {
        "unit": unit,
        "address": address,
        "value": value,
        "use_call": use_call,
    }
    return await _get_queue(modbus_hub).enqueue(priority, call_kwargs)


# -----------------------------------------------------------------------------
# Float16 helpers
# -----------------------------------------------------------------------------

def _decode_float16_from_bytes(b: bytes) -> float:
    """Decode an IEEE754 float16 from exactly 2 bytes (big-endian bit layout).

    This function expects the 2 bytes to already reflect the correct *byte order*
    of the device for a single 16-bit word.
    """
    if len(b) != 2:
        raise ValueError(f"float16 requires 2 bytes, got {len(b)}")

    bits = int.from_bytes(b, "big")
    sign = (bits >> 15) & 0x01
    exp = (bits >> 10) & 0x1F
    frac = bits & 0x03FF

    if exp == 0:
        # subnormal or zero
        if frac == 0:
            return -0.0 if sign else 0.0
        return ((-1) ** sign) * (frac / (2**10)) * 2 ** (1 - 15)

    if exp == 0x1F:
        # inf or NaN
        if frac == 0:
            return float("-inf") if sign else float("inf")
        return float("nan")

    # normal
    return ((-1) ** sign) * (1 + frac / (2**10)) * 2 ** (exp - 15)


def _encode_float16_to_bytes(value: float) -> bytes:
    """Best-effort encode of float16 to 2 bytes.

    Uses numpy if available for correct rounding. Falls back to a conservative
    approach that quantizes to float32 (not true float16) when numpy is missing.

    NOTE: This is provided mainly for symmetry and convenience.
    """
    try:
        import numpy as np  # type: ignore

        v16 = np.float16(value)
        # View as uint16 to get raw bits
        bits = int(v16.view(np.uint16))
        return bits.to_bytes(2, "big")
    except Exception:
        # Fallback: not true float16.
        # We try to approximate by mapping through float32 then taking the top 16 bits
        # would be incorrect; instead we just raise to signal we cannot do it reliably.
        raise ValueError(
            "float16 encoding requires numpy for correct IEEE754 half precision"
        )


# -----------------------------------------------------------------------------
# Word/byte order helpers
# -----------------------------------------------------------------------------

# How many 16-bit registers are needed for each supported DataType
_WORDS_NEEDED: dict[DataType, int] = {
    DataType.INT16: 1,
    DataType.UINT16: 1,
    DataType.FLOAT16: 1,
    DataType.INT32: 2,
    DataType.UINT32: 2,
    DataType.FLOAT32: 2,
    DataType.INT64: 4,
    DataType.UINT64: 4,
    DataType.FLOAT64: 4,
}


def _apply_word_order(regs: List[int], word_order: str) -> List[int]:
    """Apply word order transformation.

    word_order meanings:
      - "big":    no change
      - "little": swap words in pairs (common Modbus 'word swap')
                   * 2 words: [w0, w1] -> [w1, w0]
                   * 4 words: [w0, w1, w2, w3] -> [w1, w0, w3, w2]
                   * generic: swap adjacent pairs
      - "reverse": full reverse of the word list

    This tries to be a safer interpretation of what many devices/documentation
    call "little" word order, especially for 64-bit values.
    """
    if word_order == "big":
        return regs

    if word_order == "reverse":
        return list(reversed(regs))

    if word_order == "little":
        if len(regs) == 1:
            return regs
        # Swap adjacent pairs
        if len(regs) % 2 != 0:
            raise ValueError("word_order='little' requires an even number of words")
        swapped: List[int] = []
        for i in range(0, len(regs), 2):
            swapped.extend([regs[i + 1], regs[i]])
        return swapped

    raise ValueError(
        "word_order must be one of 'big', 'little', 'reverse'"
        f", got '{word_order}'"
    )


def _words_to_bytes(regs: Iterable[int], byte_order: str) -> bytes:
    """Convert a sequence of 16-bit words to bytes using per-word byte order."""
    if byte_order not in ("big", "little"):
        raise ValueError(f"byte_order must be 'big' or 'little', got '{byte_order}'")

    return b"".join(int(r & 0xFFFF).to_bytes(2, byte_order) for r in regs)


def _bytes_to_words(b: bytes, byte_order: str) -> List[int]:
    """Convert bytes to a list of 16-bit words interpreting per-word byte order."""
    if len(b) % 2 != 0:
        raise ValueError("Byte buffer length must be even to split into 16-bit words")

    if byte_order not in ("big", "little"):
        raise ValueError(f"byte_order must be 'big' or 'little', got '{byte_order}'")

    words: List[int] = []
    for i in range(0, len(b), 2):
        words.append(int.from_bytes(b[i : i + 2], byte_order) & 0xFFFF)
    return words


# -----------------------------------------------------------------------------
# Decode
# -----------------------------------------------------------------------------

def decode_registers_2_value(
    registers: Sequence[int],
    index: int,
    data_type: DataType,
    *,
    count: int | None = None,
    word_order: str = "big",
    byte_order: str = "big",
    encoding: str = "ascii",
    encoding_errors: str = "ignore",
) -> Any:
    """Decode a Modbus value from one or more 16-bit registers.

    Parameters
    ----------
    registers:
        Sequence of uint16 values (e.g., response.registers).
    index:
        Start index within the provided block (0-based).
    data_type:
        DataType (INT16, FLOAT32, STRING, ...).
    count:
        For STRING only: number of 16-bit registers to use.
    word_order:
        Order of 16-bit words:
          - "big":    no swap
          - "little": swap adjacent 16-bit words (word swap)
          - "reverse": reverse all words
    byte_order:
        Byte order *within each 16-bit word*:
          - "big" (default)
          - "little" (byte swap)
    encoding / encoding_errors:
        Used for STRING decoding.

    Returns
    -------
    int | float | str | Sequence[int]
        For CUSTOM: returns registers from index onward (legacy behavior).
    """

    if index < 0:
        raise IndexError(f"index must be >= 0, got {index}")

    # --- STRING: special-case using `count` registers ---
    if data_type == DataType.STRING:
        if count is None or count <= 0:
            raise ValueError("For DataType.STRING, 'count' must be > 0")

        end = index + count
        if end > len(registers):
            raise IndexError(
                f"STRING out of range: index={index}, count={count}, len={len(registers)}"
            )

        regs = [int(r) & 0xFFFF for r in registers[index:end]]
        # Apply word order too, because some devices store strings with swapped words.
        regs = _apply_word_order(regs, word_order)
        b = _words_to_bytes(regs, byte_order)
        return b.decode(encoding, errors=encoding_errors).rstrip("\x00")

    # --- CUSTOM: leave raw registers to caller (legacy behavior) ---
    if data_type == DataType.CUSTOM:
        return registers[index:]

    if data_type not in _WORDS_NEEDED:
        raise ValueError(f"Unsupported DataType: {data_type!r}")

    n_words = _WORDS_NEEDED[data_type]
    end = index + n_words
    if end > len(registers):
        raise IndexError(
            f"Out of range for {data_type.value}: "
            f"index={index}, words={n_words}, len={len(registers)}"
        )

    regs = [int(r) & 0xFFFF for r in registers[index:end]]
    regs = _apply_word_order(regs, word_order)
    b = _words_to_bytes(regs, byte_order)

    # Decode by type
    if data_type == DataType.INT16:
        return struct.unpack(">h", b)[0]
    if data_type == DataType.UINT16:
        return struct.unpack(">H", b)[0]
    if data_type == DataType.INT32:
        return struct.unpack(">i", b)[0]
    if data_type == DataType.UINT32:
        return struct.unpack(">I", b)[0]
    if data_type == DataType.INT64:
        return struct.unpack(">q", b)[0]
    if data_type == DataType.UINT64:
        return struct.unpack(">Q", b)[0]
    if data_type == DataType.FLOAT32:
        return struct.unpack(">f", b)[0]
    if data_type == DataType.FLOAT64:
        return struct.unpack(">d", b)[0]
    if data_type == DataType.FLOAT16:
        # b is 2 bytes representing the word with the chosen byte_order applied
        # We still interpret float16 bits in big-endian bit layout.
        bb = b if byte_order == "big" else bytes(reversed(b))
        return _decode_float16_from_bytes(bb)

    raise ValueError(f"Unhandled DataType: {data_type!r}")


# -----------------------------------------------------------------------------
# Encode (optional symmetry helper for writes)
# -----------------------------------------------------------------------------

def encode_value_2_registers(
    value: Union[int, float, str],
    data_type: DataType,
    *,
    count: int | None = None,
    word_order: str = "big",
    byte_order: str = "big",
    encoding: str = "ascii",
    encoding_errors: str = "strict",
) -> List[int]:
    """Encode a Python value to a list of 16-bit Modbus registers.

    This function is intended as the conceptual inverse of
    `decode_registers_2_value`.

    Parameters
    ----------
    value:
        The value to encode.
    data_type:
        Target DataType.
    count:
        For STRING: number of 16-bit registers.
    word_order / byte_order:
        See decode function.

    Returns
    -------
    list[int]
        List of uint16 words.
    """

    if data_type == DataType.CUSTOM:
        raise ValueError("CUSTOM encoding is caller-defined")

    if data_type == DataType.STRING:
        if count is None or count <= 0:
            raise ValueError("For DataType.STRING, 'count' must be > 0")

        s = str(value)
        raw = s.encode(encoding, errors=encoding_errors)
        # Pad/truncate to exactly count*2 bytes
        total_len = count * 2
        raw = raw[:total_len].ljust(total_len, b"\x00")
        # Convert bytes to words according to byte_order
        regs = _bytes_to_words(raw, byte_order)
        # Apply word order last
        regs = _apply_word_order(regs, word_order)
        return regs

    # Numeric types
    if data_type == DataType.INT16:
        b = struct.pack(">h", int(value))
    elif data_type == DataType.UINT16:
        b = struct.pack(">H", int(value))
    elif data_type == DataType.INT32:
        b = struct.pack(">i", int(value))
    elif data_type == DataType.UINT32:
        b = struct.pack(">I", int(value))
    elif data_type == DataType.INT64:
        b = struct.pack(">q", int(value))
    elif data_type == DataType.UINT64:
        b = struct.pack(">Q", int(value))
    elif data_type == DataType.FLOAT32:
        b = struct.pack(">f", float(value))
    elif data_type == DataType.FLOAT64:
        b = struct.pack(">d", float(value))
    elif data_type == DataType.FLOAT16:
        # Requires numpy for correct encoding
        bb = _encode_float16_to_bytes(float(value))
        b = bb
    else:
        raise ValueError(f"Unsupported DataType: {data_type!r}")

    # Split to words respecting byte_order inside each word
    regs = _bytes_to_words(b, byte_order)
    # Apply word-order arrangement
    regs = _apply_word_order(regs, word_order)
    return regs


# -----------------------------------------------------------------------------
# Async Modbus I/O helpers
# -----------------------------------------------------------------------------

async def async_modbus_read_area(
    modbus: ModbusHub,
    slave: int,
    register_area: RegisterArea,
):
    """Perform an async Modbus read for the specified area."""
    # _LOGGER.debug(
    #     "(unit=%s, register=%s, count=%s, function=%s) Ready to read Modbus area",
    #     slave,
    #     register_area.address,
    #     register_area.count,
    #     register_area.mdb_read_function,
    # )

    result = await _enqueue_modbus_call(
        modbus_hub=modbus,
        priority=_PRIORITY_READ,
        unit=slave,
        address=register_area.address,
        value=register_area.count,
        use_call=register_area.mdb_read_function,
    )

    return result


def _get_address_by_function(
    board_register: Register,
    board_function: Union[StrEnum, str],
) -> int:
    """Return the start address for the specified function."""
    function: RegisterFunction = board_register.functions[board_function]

    if function.address is not None:
        return function.address

    return board_register.areas[function.area].address


async def async_modbus_write_function(
    modbus_hub: ModbusHub,
    slave: int,
    register_address: int,
    value: int,
    use_call: str,
):
    """Perform an async Modbus write for the specified function."""

    # address = _get_address_by_function(board_register, board_function)

    _LOGGER.debug(
        "Modbus write function: unit=%s address=%s value=%s function=%s",
        slave,
        register_address,
        value,
        use_call,
    )

    result = await _enqueue_modbus_call(
        modbus_hub=modbus_hub,
        priority=_PRIORITY_WRITE,
        unit=slave,
        address=register_address,
        value=value,
        use_call=use_call,
    )
    return result


# -----------------------------------------------------------------------------
# Scaling + conversion helper (for value -> DataType)
# -----------------------------------------------------------------------------

_INT_RANGES = {
    DataType.INT16: (-2**15, 2**15 - 1),
    DataType.INT32: (-2**31, 2**31 - 1),
    DataType.INT64: (-2**63, 2**63 - 1),
    DataType.UINT16: (0, 2**16 - 1),
    DataType.UINT32: (0, 2**32 - 1),
    DataType.UINT64: (0, 2**64 - 1),
}


def _round_value(x: float, mode: str) -> int:
    """Round a float according to the chosen mode."""
    if mode == "nearest":
        return int(round(x))
    if mode == "floor":
        import math

        return int(math.floor(x))
    if mode == "ceil":
        import math

        return int(math.ceil(x))
    if mode == "truncate":
        return int(x)

    raise ValueError(f"Unknown rounding mode: {mode}")


def _handle_overflow(v: int, min_v: int, max_v: int, overflow: str) -> int:
    """Apply overflow policy."""
    if min_v <= v <= max_v:
        return v
    if overflow == "raise":
        raise OverflowError(f"Value {v} out of range [{min_v}, {max_v}]")
    if overflow == "clamp":
        return max(min_v, min(v, max_v))

    raise ValueError(f"Unknown overflow policy: {overflow}")


def _to_float32(x: float) -> float:
    return struct.unpack("!f", struct.pack("!f", float(x)))[0]


def _to_float64(x: float) -> float:
    return struct.unpack("!d", struct.pack("!d", float(x)))[0]


def _to_float16(x: float) -> float:
    try:
        import numpy as np  # type: ignore

        return float(np.float16(x))
    except Exception:
        # Best-effort fallback: not true float16
        return _to_float32(x)



IntDataType: TypeAlias = Literal[
    # DataType.INT8, DataType.UINT8,
    DataType.INT16, DataType.UINT16,
    DataType.INT32, DataType.UINT32,
    DataType.INT64, DataType.UINT64,
]

FloatDataType: TypeAlias = Literal[
    DataType.FLOAT16,
    DataType.FLOAT32,
    DataType.FLOAT64
]

def is_int_dtype(dt: DataType) -> TypeGuard[IntDataType]:
    return dt in _INT_RANGES


@overload
def convert_native_2_register_value(
    value: float,
    scale: float,
    dtype: IntDataType,
    *,
    rounding: str = "nearest",
    overflow: str = "raise",
) -> int: ...

@overload
def convert_native_2_register_value(
    value: float,
    scale: float,
    dtype: FloatDataType,
    *,
    rounding: str = "nearest",
    overflow: str = "raise",
) -> float: ...

@overload
def convert_native_2_register_value(
    value: float,
    scale: float,
    dtype: Literal[DataType.STRING],
    *,
    rounding: str = "nearest",
    overflow: str = "raise",
) -> str: ...

@overload
def convert_native_2_register_value(
    value: float,
    scale: float,
    dtype: Literal[DataType.CUSTOM],
    *,
    rounding: str = "nearest",
    overflow: str = "raise",
) -> float: ...


def convert_native_2_register_value(
    value: float,
    scale: float,
    dtype: DataType,
    *,
    rounding: str = "nearest",
    overflow: str = "raise",
) -> Union[int, float, str]:
    scaled = float(value) * float(scale)

    if dtype == DataType.CUSTOM:
        return scaled

    if dtype == DataType.STRING:
        return str(scaled)

    if dtype in _INT_RANGES:
        min_v, max_v = _INT_RANGES[dtype]
        iv = _round_value(scaled, rounding)
        iv = _handle_overflow(iv, min_v, max_v, overflow)
        return iv

    if dtype == DataType.FLOAT16:
        return _to_float16(scaled)
    if dtype == DataType.FLOAT32:
        return _to_float32(scaled)
    if dtype == DataType.FLOAT64:
        return _to_float64(scaled)

    raise ValueError(f"Unsupported DataType: {dtype}")
