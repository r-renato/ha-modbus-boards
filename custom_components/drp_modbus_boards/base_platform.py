"""Base implementation for all modbus platforms."""
from __future__ import annotations

import time
from random import randint
import asyncio
from abc import abstractmethod
from collections.abc import Callable
from datetime import datetime, timedelta
import logging
import struct
from typing import Any, cast

from pymodbus.pdu import ModbusResponse
from homeassistant.const import (
    CONF_ADDRESS,
    CONF_COMMAND_OFF,
    CONF_COMMAND_ON,
    CONF_COUNT,
    CONF_DELAY,
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_OFFSET,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    CONF_STRUCTURE,
    CONF_UNIQUE_ID,
    STATE_OFF,
    STATE_ON,
    EVENT_HOMEASSISTANT_START,
    Platform,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity, ToggleEntity
from homeassistant.helpers.event import async_track_state_change_event, async_call_later, async_track_time_interval
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    CALL_TYPE_COIL,
    CALL_TYPE_DISCRETE,
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_REGISTER_INPUT,
    CALL_TYPE_WRITE_COIL,
    CALL_TYPE_WRITE_COILS,
    CALL_TYPE_WRITE_REGISTER,
    CALL_TYPE_WRITE_REGISTERS,
    CALL_TYPE_X_COILS,
    CALL_TYPE_X_REGISTER_HOLDINGS,
    CONF_DATA_TYPE,
    CONF_DEVICE_ADDRESS,
    CONF_INPUT_TYPE,
    CONF_LAZY_ERROR,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_NAN_VALUE,
    CONF_PRECISION,
    CONF_SCALE,
    CONF_SLAVE_COUNT,
    CONF_STATE_OFF,
    CONF_STATE_ON,
    CONF_SWAP,
    CONF_SWAP_BYTE,
    CONF_SWAP_WORD,
    CONF_SWAP_WORD_BYTE,
    CONF_VERIFY,
    CONF_VIRTUAL_COUNT,
    CONF_WRITE_TYPE,
    CONF_ZERO_SUPPRESS,
    MODBUS_DOMAIN,
    SIGNAL_START_ENTITY,
    SIGNAL_STOP_ENTITY,
    DataType,
)
from .boards_const import (
    CONF_SWITCH_CONSTRAINT,
    MODBUS_DOMAIN as DOMAIN,
    CONF_BOARD,
    BOARDS,
    METADATA,
    # BLOCK_NAME,
    # BLOCK_NDX,
    # METADATA,
    # ADDRESS,
    # QUANTITY,
    # FUNCTION,
    # SWITCH_STATE_OPEN,
    # SWITCH_STATE_CLOSE,
    # COMMAND_ADDRESS,
    # COMMAND_WRITE_TYPE,
    # COMMAND_OPEN,
    # COMMAND_CLOSE,

    # BLK_ADDRESS,
    # BLK_QUANTITY,
    # BLK_FUNCTION,
    # BLK_DATA_TYPE,
    # BLK_STATE_CLOSE,
    # BLK_STATE_OPEN,

    # RBD_BLOCK_NAME,
    # RBD_BLOCK_NDX,
    # RBD_PRECISION,
    # RBD_SCALE,
    # RBD_STATE_CLASS,
    # RBD_DEVICE_CLASS,
    # RBD_UNIT_OF_MEASURE,
    # RWBD_ADDRESS,
    # RWBD_FUNCTION,
    # RWBD_SCALE,
    # RWBD_MIN,
    # RWBD_MAX,
    # RWBD_STEP,
    # RWBD_NMODE,
    # RWBD_GUIDE,

    # WBD_BLOCK_NAME,
    # WBD_BLOCK_NDX,
    # WBD_ADDRESS,
    # WBD_FUNCTION,
    # WBD_COMMAND_CLOSE,
    # WBD_COMMAND_OPEN,

    STRUCTUREMAP,
    BoardBlock,
    BoardBlockRegIdx,
    SwitchRegIdx,
    NumericRegIdx,
)
from .modbus import ModbusHub
# from .base_platform import BoardsBasePlatform, BoardsBaseStructPlatform

PARALLEL_UPDATES = 1
_LOGGER = logging.getLogger(__name__)

class DataProcessing:
    @staticmethod
    def _process_raw_value(
        entry: float | int | str | bytes,
        _scale: float | int,
        _precision: float | int,
    ) -> float | int | str | bytes | None:
        """Process value from sensor with NaN handling, scaling, offset, min/max etc."""
        # if self._nan_value and entry in (self._nan_value, -self._nan_value):
        #     return None
        # if isinstance(entry, bytes):
        #     return entry
        # val: float | int = round(_scale * entry + self._offset, _precision)
        # if self._min_value is not None and val < self._min_value:
        #     return self._min_value
        # if self._max_value is not None and val > self._max_value:
        #     return self._max_value
        # if self._zero_suppress is not None and abs(val) <= self._zero_suppress:
        #     return 0
        # return val
        return round(_scale * entry, _precision)

    @staticmethod
    def _unpack_structure_result( 
        registers: list[int],
        _data_type: str,
        _scale: float | int,
        _precision: float | int,
    ) -> str | None:
        """Convert registers to proper result."""

        # if self._swap:
        #     registers = self._swap_registers(registers, self._slave_count)
        byte_string = b"".join([x.to_bytes(2, byteorder="big") for x in registers])
        if _data_type == DataType.STRING:
            return byte_string.decode()
        if byte_string == b"nan\x00":
            return None

        try:
            _structure = STRUCTUREMAP[_data_type]
            val = struct.unpack(_structure, byte_string)
        except struct.error as err:
            recv_size = len(registers) * 2
            msg = f"Received {recv_size} bytes, unpack error {err}"
            _LOGGER.error(msg)
            return None
        if len(val) > 1:
            # Apply scale, precision, limits to floats and ints
            v_result = []
            for entry in val:
                v_temp = DataProcessing._process_raw_value(entry, _scale, _precision)
                if v_temp is None:
                    v_result.append("0")
                else:
                    v_result.append(str(v_temp))
            return ",".join(map(str, v_result))

        # Apply scale, precision, limits to floats and ints
        return DataProcessing._process_raw_value(val[0], _scale, _precision)

    @staticmethod
    def unpack_data( 
            registers: list[int],
            ndx_start: int,
            _data_type: str,
            _scale: float | int,
            _precision: float | int,
    ) -> str | None:
        """Convert registers to proper result."""

        # _LOGGER.debug( "async_update '%s' '%s' %s",
        #     str(registers), str(ndx_start), str(_data_type)
        # )

        posix = (ndx_start,)
        if _data_type in (DataType.INT8, DataType.UINT8):
            posix = (ndx_start,)
        elif _data_type in (DataType.INT16, DataType.UINT16, DataType.FLOAT16):
            posix = (ndx_start,)
        elif _data_type in (DataType.INT32, DataType.UINT32, DataType.FLOAT32):
            posix = (ndx_start, ndx_start + 1)

        _LOGGER.debug( "unpack_data '%s' '%s' %s",
            str(registers), str(_data_type), str(posix)
        )
        subset_data = [registers[i] for i in posix]
        _LOGGER.debug( "unpack_data reg:'%s' dtype:'%s' ndx:%s, subset:'%s'",
            str(registers), str(_data_type), str(posix), str(subset_data)
        )
        result_list = DataProcessing._unpack_structure_result(subset_data,_data_type,_scale,_precision)

        return result_list


class BasePlatform(Entity):
    """Base for readonly platforms."""

    def __init__(
        self, hass: HomeAssistant, hub: ModbusHub, entry: dict[str, Any]
    ) -> None:
        """Initialize the Modbus binary sensor."""

        if CONF_LAZY_ERROR in entry:
            async_create_issue(
                hass,
                DOMAIN,
                "removed_lazy_error_count",
                breaks_in_ha_version="2024.7.0",
                is_fixable=False,
                severity=IssueSeverity.WARNING,
                translation_key="removed_lazy_error_count",
                translation_placeholders={
                    "config_key": "lazy_error_count",
                    "integration": DOMAIN,
                    "url": "https://www.home-assistant.io/integrations/modbus",
                },
            )
            _LOGGER.warning(
                "`close_comm_on_error`: is deprecated and will be removed in version 2024.4"
            )

            _LOGGER.warning(
                "`lazy_error_count`: is deprecated and will be removed in version 2024.7"
            )

        self._hub = hub
        self._slave = entry.get(CONF_SLAVE, None) or entry.get(CONF_DEVICE_ADDRESS, 0)
        # self._address = int(entry[CONF_ADDRESS])
        self._input_type = entry[CONF_INPUT_TYPE]
        self._value: str | None = None
        self._scan_interval = int(entry[CONF_SCAN_INTERVAL])
        self._call_active = False
        self._cancel_timer: Callable[[], None] | None = None
        self._cancel_call: Callable[[], None] | None = None

        self._attr_unique_id = entry.get(CONF_UNIQUE_ID)
        self._attr_name = entry[CONF_NAME]
        self._attr_should_poll = False
        self._attr_device_class = entry.get(CONF_DEVICE_CLASS)
        self._attr_available = True
        self._attr_unit_of_measurement = None

        def get_optional_numeric_config(config_name: str) -> int | float | None:
            if (val := entry.get(config_name)) is None:
                return None
            assert isinstance(
                val, (float, int)
            ), f"Expected float or int but {config_name} was {type(val)}"
            return val

        self._min_value = get_optional_numeric_config(CONF_MIN_VALUE)
        self._max_value = get_optional_numeric_config(CONF_MAX_VALUE)
        self._nan_value = entry.get(CONF_NAN_VALUE, None)
        self._zero_suppress = get_optional_numeric_config(CONF_ZERO_SUPPRESS)

    @abstractmethod
    async def async_update(self, now: datetime | None = None) -> None:
        """Virtual function to be overwritten."""

    @callback
    def async_run(self) -> None:
        """Remote start entity."""
        self.async_hold(update=False)
        self._cancel_call = async_call_later(
            self.hass, timedelta(milliseconds=100), self.async_update
        )
        if self._scan_interval > 0:
            self._cancel_timer = async_track_time_interval(
                self.hass, self.async_update, timedelta(seconds=self._scan_interval)
            )
        self._attr_available = True
        self.async_write_ha_state()

    @callback
    def async_hold(self, update: bool = True) -> None:
        """Remote stop entity."""
        if self._cancel_call:
            self._cancel_call()
            self._cancel_call = None
        if self._cancel_timer:
            self._cancel_timer()
            self._cancel_timer = None
        if update:
            self._attr_available = False
            self.async_write_ha_state()

    async def async_base_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        self.async_run()
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_STOP_ENTITY, self.async_hold)
        )
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_START_ENTITY, self.async_run)
        )

class BoardsBasePlatform(BasePlatform):
    """Base for readonly platforms."""

    def __init__(
        self, hass: HomeAssistant, hub: ModbusHub, config: dict[str, Any], platform: str, device_name: str
    ) -> None:
        """Initialize the Modbus binary sensor."""
        super().__init__(hass, hub, config)
        self._attr_available = False
        self._state_constraint = 'on'
        self._switch_constraint = config.get(CONF_SWITCH_CONSTRAINT, None)

        self._attr_board = config.get(CONF_BOARD)
        self._attr_metadata = (BOARDS[self._attr_board])[METADATA]
        self._attr_sensor_name = device_name
        self._attr_platform = platform
        self._attr_platform_registers = (BOARDS[self._attr_board])[platform]
        self._attr_sensor_registers = self._attr_platform_registers[self._attr_sensor_name]
        self._attr_board_blocks = {}

        self._attr_manufacturer = None
        self._attr_model = None
        self._platform_ready = False

        self._lazy_error_count = 3
        self._lazy_errors = self._lazy_error_count

    async def async_base_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_base_added_to_hass()

        if self._switch_constraint:
            self.async_on_remove(
                async_track_state_change_event(self.hass, self._switch_constraint, self._async_component_changed)
            )
        
        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self._async_update_switch_constraint_status)

    async def _async_update_switch_constraint_status(self, event) -> None:
        """Handle entity which will be added."""
        if self._switch_constraint:
            self._old_state_constraint = self._state_constraint
            self._state_constraint = self.hass.states.get(self._switch_constraint).state

        if self._state_constraint == 'on':
            self._attr_available = True

        self.async_write_ha_state()
        self._platform_ready = True

        async_call_later(
            self.hass, timedelta(milliseconds=100), self.async_update
        )

    async def _async_component_changed(self, event):
        """Handle sensor changes."""
        self._old_state_constraint = self._state_constraint
        new_state = event.data.get("new_state")
        self._state_constraint = new_state.state

        if self._state_constraint == 'on':
            self._attr_available = True
            async_call_later(self.hass, 5, self.async_update)
        else:
            self._attr_available = False
        
        self.async_write_ha_state()

        _LOGGER.debug( 'async_component_changed: slave:%d, constraint:%s', self._slave, str(self._state_constraint) )

    async def async_board_read_data(self, platform: str)-> bool:
        done = False

        for block in BoardBlock:
            if block in self._attr_platform_registers:
                block_register = self._attr_platform_registers[block]
                self._cancel_call = None
                
                # _LOGGER.debug( "async_board_read_data %s %s slave:%s addr:%s qty:%s fn:%s", 
                #             self._attr_board, platform, 
                #             str(self._slave), str(block_register[BLK_ADDRESS]), str(block_register[BLK_QUANTITY]), 
                #             str(block_register[BLK_FUNCTION])
                # )             
                raw_result = await self._hub.async_pb_call(
                    self._slave, 
                    block_register[BoardBlockRegIdx.BLOCK_ADDRESS], 
                    block_register[BoardBlockRegIdx.BLOCK_QTY], 
                    block_register[BoardBlockRegIdx.BLOCK_FUNCTION]
                )
                self._attr_board_blocks[block] = raw_result
 
                done = True if raw_result else False

                _LOGGER.debug( "async_board_read_data %s %s slave:%s addr:%s qty:%s fn:%s res:%s", 
                            self._attr_board, platform, 
                            str(self._slave), str(block_register[BoardBlockRegIdx.BLOCK_ADDRESS]),
                            str(block_register[BoardBlockRegIdx.BLOCK_QTY]), 
                            str(block_register[BoardBlockRegIdx.BLOCK_FUNCTION]), 
                            str(str(raw_result.registers) if raw_result is not None else "None")
                )  
        
        return done

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        data: dict[str, Any] = { 
            CONF_SLAVE : self._slave,
            "coordinator id" : self._slave_count,
        }

        if self._attr_manufacturer:
            data[ "manufacturer" ] = self._attr_manufacturer
        if self._attr_model:
            data[ "model" ] = self._attr_model

        if Platform.SWITCH == self._attr_platform and len(self._attr_sensor_registers) > SwitchRegIdx.GUIDE:
            data[ "guide" ] = self._attr_sensor_registers[SwitchRegIdx.GUIDE]

        if Platform.NUMBER == self._attr_platform and len(self._attr_sensor_registers) > NumericRegIdx.GUIDE:
            data[ "guide" ] = self._attr_sensor_registers[NumericRegIdx.GUIDE]

        return data

class BaseStructPlatform(BoardsBasePlatform, RestoreEntity):
    """Base class representing a sensor/climate."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, device_name: str) -> None:
        """Initialize the switch."""
        super().__init__(hass, hub, config, platform, device_name)
        self._swap = config[CONF_SWAP]
        self._data_type = config[CONF_DATA_TYPE]
        self._structure: str = config[CONF_STRUCTURE]
        self._scale = config[CONF_SCALE]
        self._precision = config.get(CONF_PRECISION, 2 if self._scale < 1 else 0)
        self._offset = config[CONF_OFFSET]
        self._slave_count = config.get(CONF_SLAVE_COUNT, None) or config.get(
            CONF_VIRTUAL_COUNT, 0
        )
        self._slave_size = self._count = config[CONF_COUNT]

    def _swap_registers(self, registers: list[int], slave_count: int) -> list[int]:
        """Do swap as needed."""
        if slave_count:
            swapped = []
            for i in range(0, self._slave_count + 1):
                inx = i * self._slave_size
                inx2 = inx + self._slave_size
                swapped.extend(self._swap_registers(registers[inx:inx2], 0))
            return swapped
        if self._swap in (CONF_SWAP_BYTE, CONF_SWAP_WORD_BYTE):
            # convert [12][34] --> [21][43]
            for i, register in enumerate(registers):
                registers[i] = int.from_bytes(
                    register.to_bytes(2, byteorder="little"),
                    byteorder="big",
                    signed=False,
                )
        if self._swap in (CONF_SWAP_WORD, CONF_SWAP_WORD_BYTE):
            # convert [12][34] ==> [34][12]
            registers.reverse()
        return registers

    def _process_raw_value(self, entry: float | int | str | bytes) -> str | None:
        """Process value from sensor with NaN handling, scaling, offset, min/max etc."""
        if self._nan_value and entry in (self._nan_value, -self._nan_value):
            return None
        if isinstance(entry, bytes):
            return entry.decode()
        if entry != entry:  # noqa: PLR0124
            # NaN float detection replace with None
            return None
        val: float | int = self._scale * entry + self._offset
        if self._min_value is not None and val < self._min_value:
            return str(self._min_value)
        if self._max_value is not None and val > self._max_value:
            return str(self._max_value)
        if self._zero_suppress is not None and abs(val) <= self._zero_suppress:
            return "0"
        if self._precision == 0:
            return str(int(round(val, 0)))
        return f"{float(val):.{self._precision}f}"

    def unpack_structure_result(self, registers: list[int]) -> str | None:
        """Convert registers to proper result."""

        if self._swap:
            registers = self._swap_registers(registers, self._slave_count)
        byte_string = b"".join([x.to_bytes(2, byteorder="big") for x in registers])
        if self._data_type == DataType.STRING:
            return byte_string.decode()
        if byte_string == b"nan\x00":
            return None

        try:
            val = struct.unpack(self._structure, byte_string)
        except struct.error as err:
            recv_size = len(registers) * 2
            msg = f"Received {recv_size} bytes, unpack error {err}"
            _LOGGER.error(msg)
            return None
        if len(val) > 1:
            # Apply scale, precision, limits to floats and ints
            v_result = []
            for entry in val:
                v_temp = self._process_raw_value(entry)
                if v_temp is None:
                    v_result.append("0")
                else:
                    v_result.append(str(v_temp))
            return ",".join(map(str, v_result))

        # Apply scale, precision, limits to floats and ints
        return self._process_raw_value(val[0])

class BoardsBaseStructPlatform(BaseStructPlatform):
    """Base class representing a sensor/climate."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, device_name: str) -> None:
        """Initialize the switch."""
        config[CONF_SWAP] = 'none'
        config[CONF_DATA_TYPE] = None
        config[CONF_STRUCTURE] = None
        config[CONF_SCALE] = 1
        config[CONF_OFFSET] = 0
        config[CONF_COUNT] = 0
        super().__init__(hass, hub, config, platform, device_name)

    def _process_raw_value(
        self,
        entry: float | int | str | bytes,
        _scale: float | int,
        _precision: float | int,
    ) -> float | int | str | bytes | None:
        """Process value from sensor with NaN handling, scaling, offset, min/max etc."""
        if self._nan_value and entry in (self._nan_value, -self._nan_value):
            return None
        if isinstance(entry, bytes):
            return entry
        val: float | int = round(_scale * entry + self._offset, _precision)
        if self._min_value is not None and val < self._min_value:
            return self._min_value
        if self._max_value is not None and val > self._max_value:
            return self._max_value
        if self._zero_suppress is not None and abs(val) <= self._zero_suppress:
            return 0
        return val

    def unpack_structure_result(self, 
        registers: list[int],
        _data_type: str,
        _scale: float | int,
        _precision: float | int,
    ) -> str | None:
        """Convert registers to proper result."""

        # if self._swap:
        #     registers = self._swap_registers(registers, self._slave_count)
        byte_string = b"".join([x.to_bytes(2, byteorder="big") for x in registers])
        if _data_type == DataType.STRING:
            return byte_string.decode()
        if byte_string == b"nan\x00":
            return None

        try:
            _structure = STRUCTUREMAP[_data_type]
            val = struct.unpack(_structure, byte_string)
        except struct.error as err:
            recv_size = len(registers) * 2
            msg = f"Received {recv_size} bytes, unpack error {err}"
            _LOGGER.error(msg)
            return None
        if len(val) > 1:
            # Apply scale, precision, limits to floats and ints
            v_result = []
            for entry in val:
                v_temp = self._process_raw_value(entry, _scale, _precision)
                if v_temp is None:
                    v_result.append("0")
                else:
                    v_result.append(str(v_temp))
            return ",".join(map(str, v_result))

        # Apply scale, precision, limits to floats and ints
        return self._process_raw_value(val[0], _scale, _precision)

class BaseSwitch(BoardsBasePlatform, ToggleEntity, RestoreEntity):
    """Base class representing a Modbus switch."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, switch_name: str) -> None:
        """Initialize the switch."""
        config[CONF_INPUT_TYPE] = ""
        super().__init__(hass, hub, config, platform, switch_name)
        self._attr_is_on = False
        convert = {
            CALL_TYPE_REGISTER_HOLDING: (
                CALL_TYPE_REGISTER_HOLDING,
                CALL_TYPE_WRITE_REGISTER,
            ),
            CALL_TYPE_DISCRETE: (
                CALL_TYPE_DISCRETE,
                None,
            ),
            CALL_TYPE_REGISTER_INPUT: (
                CALL_TYPE_REGISTER_INPUT,
                None,
            ),
            CALL_TYPE_COIL: (CALL_TYPE_COIL, CALL_TYPE_WRITE_COIL),
            CALL_TYPE_X_COILS: (CALL_TYPE_COIL, CALL_TYPE_WRITE_COILS),
            CALL_TYPE_X_REGISTER_HOLDINGS: (
                CALL_TYPE_REGISTER_HOLDING,
                CALL_TYPE_WRITE_REGISTERS,
            ),
        }
        self._write_type = cast(str, convert[config[CONF_WRITE_TYPE]][1])
        self.command_on = config[CONF_COMMAND_ON]
        self._command_off = config[CONF_COMMAND_OFF]
        if CONF_VERIFY in config:
            if config[CONF_VERIFY] is None:
                config[CONF_VERIFY] = {}
            self._verify_active = True
            self._verify_delay = config[CONF_VERIFY].get(CONF_DELAY, 0)
            self._verify_address = config[CONF_VERIFY].get(
                CONF_ADDRESS, config[CONF_ADDRESS]
            )
            self._verify_type = convert[
                config[CONF_VERIFY].get(CONF_INPUT_TYPE, config[CONF_WRITE_TYPE])
            ][0]
            self._state_on = config[CONF_VERIFY].get(CONF_STATE_ON, self.command_on)
            self._state_off = config[CONF_VERIFY].get(CONF_STATE_OFF, self._command_off)
        else:
            self._verify_active = False

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()
        if state := await self.async_get_last_state():
            if state.state == STATE_ON:
                self._attr_is_on = True
            elif state.state == STATE_OFF:
                self._attr_is_on = False

    async def async_turn(self, command: int) -> None:
        """Evaluate switch result."""
        result = await self._hub.async_pb_call(
            self._slave, self._address, command, self._write_type
        )
        if result is None:
            self._attr_available = False
            self.async_write_ha_state()
            return

        self._attr_available = True
        if not self._verify_active:
            self._attr_is_on = command == self.command_on
            self.async_write_ha_state()
            return

        if self._verify_delay:
            async_call_later(self.hass, self._verify_delay, self.async_update)
        else:
            await self.async_update()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set switch off."""
        await self.async_turn(self._command_off)

    async def async_update(self, now: datetime | None = None) -> None:
        """Update the entity state."""
        # remark "now" is a dummy parameter to avoid problems with
        # async_track_time_interval
        if not self._verify_active:
            self._attr_available = True
            self.async_write_ha_state()
            return

        # do not allow multiple active calls to the same platform
        if self._call_active:
            return
        self._call_active = True
        result = await self._hub.async_pb_call(
            self._slave, self._verify_address, 1, self._verify_type
        )
        self._call_active = False
        if result is None:
            self._attr_available = False
            self.async_write_ha_state()
            return

        self._attr_available = True
        if self._verify_type in (CALL_TYPE_COIL, CALL_TYPE_DISCRETE):
            self._attr_is_on = bool(result.bits[0] & 1)
        else:
            value = int(result.registers[0])
            if value == self._state_on:
                self._attr_is_on = True
            elif value == self._state_off:
                self._attr_is_on = False
            elif value is not None:
                _LOGGER.error(
                    (
                        "Unexpected response from modbus device slave %s register %s,"
                        " got 0x%2x"
                    ),
                    self._slave,
                    self._verify_address,
                    value,
                )
        self.async_write_ha_state()

class BoardsBaseSwitch(BaseSwitch):
    """Base class representing a sensor/climate."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, switch_name: str) -> None:
        super().__init__(hass, hub, config, platform, switch_name)
        self._scan_interval = 90
        self._update_lock = asyncio.Lock()
        self._update_lock_flag = False
        self._command_lock = asyncio.Lock()
        self._command_lock_flag = False
        self._command_start_time = time.perf_counter()

        self._address = self._attr_sensor_registers[SwitchRegIdx.REGW_ADDRESS]
        self._write_type = self._attr_sensor_registers[SwitchRegIdx.REGW_FUNCTION]
        self.command_on = self._attr_sensor_registers[SwitchRegIdx.REGW_COMMAND_CLOSE]
        self._command_off = self._attr_sensor_registers[SwitchRegIdx.REGW_COMMAND_OPEN]

        self._state_on = (self._attr_platform_registers[BoardBlock.REGISTERS_BLOCK_1])[SwitchRegIdx.BLOCK_STATE_CLOSE]
        self._state_off = (self._attr_platform_registers[BoardBlock.REGISTERS_BLOCK_1])[SwitchRegIdx.BLOCK_STATE_OPEN]

    def _decode_state(self, sensor_data) -> True | False | None:
        result = None

        if sensor_data.registers:
            result_data = DataProcessing.unpack_data( 
                sensor_data.registers,
                self._attr_sensor_registers[SwitchRegIdx.BLOCK_DATA_NDX],
                DataType.INT16,
                1,
                0,
            )
        elif sensor_data.bits:
            result_data = sensor_data.bits[self._attr_sensor_registers[SwitchRegIdx.BLOCK_DATA_NDX]]

            # _LOGGER.debug( "_decode_state '%s' slave:'%s'::%s data:'%s' result:'%s'", 
            #                   self._attr_board, self._slave, str(self._slave_count),
            #                   str(sensor_data.registers if sensor_data.registers else sensor_data.bits), str(result_data))
            
        if result_data is None:
            return None

        if result_data == self._state_on:
            result = True
        elif result_data == self._state_off:
            result = False
        _LOGGER.debug( "_decode_state '%s' slave:'%s'::%s data:'%s' result:'%s' %s %s %s", 
                            self._attr_board, self._slave, str(self._slave_count),
                            str(sensor_data.registers if sensor_data.registers else sensor_data.bits), 
                            str(result), str(self._state_on), str(self._state_off), str(result_data))
        return result
    
    async def _async_turn_off(self, now: datetime | None = None):
        await self.async_turn(self._command_off)

    async def _async_turn_on(self, now: datetime | None = None):
        await self.async_turn(self.command_on)

    async def async_turn(self, command: int) -> None:
        if self._command_lock_flag and (time.perf_counter()-self._command_start_time < 60):
            return

        if self._state_constraint != 'on':
            self._attr_available = False
            self._attr_native_value = None
            if self._coordinator:
                self._coordinator.async_set_updated_data(None)
            self.async_write_ha_state()
            return  
        
        async with self._command_lock:
            self._command_start_time = time.perf_counter()
            self._command_lock_flag = True

            result = await self._hub.async_pb_call(
                self._slave, self._address, command, self._write_type
            )

            if result is None:
                if self._lazy_errors:
                    self._lazy_errors -= 1
                    self._cancel_call = async_call_later(
                        self.hass, 
                        timedelta(seconds=1), 
                        (self._async_turn_on if command == self.command_on else self._async_turn_off)
                    )
                    self._update_lock_flag = False
                    return
                self._attr_available = False
                self._command_lock_flag = False
                self.async_write_ha_state()
                _LOGGER.debug( "async_turn (%d) '%s' slave:'%s' Error writing data. (%s)", 
                    round(time.perf_counter()-self._command_start_time, 2), self._attr_board, self._slave, str(result))
                return

            self._attr_available = True 
            if command == self.command_on:
                self._attr_is_on = True
            elif command == self._command_off:
                self._attr_is_on = False
            else:
                self._attr_available = False

            _LOGGER.debug( 'async_turn (%d) slave:%d, address:%d, write_type:%s, command:%s, result:%s', 
                round(time.perf_counter()-self._command_start_time, 2),
                self._slave, self._address, str(self._write_type), str(command), 
                str(result.registers if result.registers else result.bits)
            )
            
            self._command_lock_flag = False
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set switch off."""
        await self._async_turn_off()

class BoardsBaseSlaveSwitch(
    BoardsBaseSwitch,
    RestoreEntity,
):
    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, switch_name: str) -> None:
        super().__init__(hass, hub, config, platform, switch_name)

    async def async_update(self, now: datetime | None = None) -> None:
        return
            
    async def async_added_to_hass(self) -> None:
        return
    
class BoardsBaseNumber(BoardsBasePlatform, RestoreEntity):
    """Base class representing a sensor/climate."""

    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, number_name: str) -> None:
        super().__init__(hass, hub, config, platform, number_name)
        self._scan_interval = 90
        self._update_lock = asyncio.Lock()
        self._update_lock_flag = False
        self._command_lock = asyncio.Lock()
        self._command_lock_flag = False

        self._address = self._attr_sensor_registers[NumericRegIdx.REGW_ADDRESS]
        self._write_type = self._attr_sensor_registers[NumericRegIdx.REGW_FUNCTION]
        self._write_scale = self._attr_sensor_registers[NumericRegIdx.REGW_SCALE]
    
    async def async_set_modbus_value(self, value: float) -> None:
        if self._command_lock_flag:
            return

        async with self._command_lock:
            self._command_lock_flag = True

            write_value = int(value * self._write_scale)

            _LOGGER.debug( 'async_set_modbus_value slave:%d, address:%d, write_type:%s, value:%d,', 
                self._slave, self._address, str(self._write_type), write_value )
        
        # builder = BinaryPayloadBuilder(byteorder=Endian.LITTLE, wordorder=Endian.BIG)
        # builder.add_32bit_float(value)
        # payload = builder.build()

        # payload = int(value * 10)
        # client.write_registers(0,payload,count=2,unit= 1,skip_encode = True)
        # _LOGGER.debug( '### Number async_set_modbus_value pre slave:%d, address:%d, write_type:%s, value:%d, payload:%s', 
        #      self._slave, self._address, str(self._write_type), value, str(payload) )
            result = await self._hub.async_pb_call(
                self._slave, self._address, write_value, self._write_type
            )
            _LOGGER.debug( '### Number async_set_modbus_value post slave:%d, address:%d, write_type:%s, value:%s, result :: %s', 
                self._slave, self._address, str(self._write_type), write_value, str(result) )
        
            if result is None:
                self._attr_available = False
                self.async_write_ha_state()
                self._command_lock_flag = False
                return
        
            self._attr_native_value = value
            self._attr_available = True
            self._command_lock_flag = False
 
class BoardsBaseSlaveNumber(
    BoardsBaseNumber, RestoreEntity
):
    def __init__(self, hass: HomeAssistant, hub: ModbusHub, config: dict, platform: str, number_name: str) -> None:
        super().__init__(hass, hub, config, platform, number_name)

    async def async_update(self, now: datetime | None = None) -> None:
        return
            
    async def async_added_to_hass(self) -> None:
        return
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        data: dict[str, Any] = { 
            CONF_SLAVE : self._slave,
            "coordinated slave id" : self._slave_count,
        }

        if self._attr_manufacturer:
            data[ "manufacturer" ] = self._attr_manufacturer
        if self._attr_model:
            data[ "model" ] = self._attr_model

        if Platform.NUMBER == self._attr_platform and len(self._attr_sensor_registers) > NumericRegIdx.GUIDE:
            data[ "guide" ] = self._attr_sensor_registers[NumericRegIdx.GUIDE]

        return data