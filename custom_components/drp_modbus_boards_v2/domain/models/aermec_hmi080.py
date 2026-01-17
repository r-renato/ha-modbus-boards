"""Registers mapping for Aermec HMI080 board."""
from __future__ import annotations

from homeassistant.components.number import NumberMode
from homeassistant.const import Platform, UnitOfTime
from homeassistant.components.modbus import const as modbus_const
from homeassistant.components.modbus.const import (
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_COIL,
    CALL_TYPE_WRITE_COILS,
    CALL_TYPE_WRITE_REGISTERS,
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
    RegisterFunction,
    RegisterFunctionRead,
    RegisterFunctionWrite,
)
from ..enums import (
    AermecHMI080BinarySensorFunction,
    AermecHMI080NumberFunction,
    AermecHMI080SensorFunction,
    AermecHMI080SwitchFunction,
    Board,
    RegisterAreaName,
)

# Create a new tuple adding our entry
ensure_number_in_platforms(modbus_const, CONF_NUMBERS)

####### ####### ####### ####### #######
#   AERMEC HMI080
####### ####### ####### ####### #######


@register_board(Board.AERMEC_HMI080)
def _aermec_hmi080_regs() -> BoardDefinition:
    return BoardDefinition(
        metadata=Metadata(
            name="Reversible air/water heat pump single-phase inverter",
            manufacturer="aermec",
            model="hmi080",
        ),
        areas={
            # State variables (Bit 0 .. Bit 199)
            RegisterAreaName.AREA_A: RegisterArea(
                address=0x00,
                count=199,

                mdb_read_function=CALL_TYPE_COIL,
                mdb_write_function=CALL_TYPE_WRITE_COILS,
                
                state_on=True,
                state_off=False,
                
                command_on=True,
                command_off=False,
            ),
            # Analog variables (Word 117 .. Word 137)
            RegisterAreaName.AREA_B: RegisterArea(
                address=0x75,
                count=21,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                
                data_type=DataType.INT16,
            ),
            # Analog control: Word 42 (On/Off)
            RegisterAreaName.AREA_C: RegisterArea(
                address=0x2A,
                count=2,
                registry_area_shift=-0x2A,

                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTERS,
                
                data_type=DataType.UINT16,
                
                state_on=0xAA,
                state_off=0x55,
                
                command_on=0xAA,
                command_off=0x55,
            ),
            # Analog variables (Word 0 .. Word 43)
            RegisterAreaName.AREA_D: RegisterArea(
                address=0x00,
                count=44,
                
                mdb_read_function=CALL_TYPE_REGISTER_HOLDING,
                mdb_write_function=CALL_TYPE_WRITE_REGISTERS,
                
                data_type=DataType.UINT16,
            ),
        },
        registers={
            #
            # BINARY SENSOR (Bit registers)
            #
            Platform.BINARY_SENSOR: Register(
                functions={
                    AermecHMI080BinarySensorFunction.HEAT_2_WAY_VALVE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x26,
                        description=(
                            "Heat 2-way valve state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_IDU: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x40,
                        description=(
                            "Communication error between wired controller and IDU. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_ODU: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x41,
                        description=(
                            "Communication error between wired controller and ODU. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COM_ERROR_BETWEEN_THE_WIRED_CTRL_AND_DRIVE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x42,
                        description=(
                            "Communication error between wired controller and drive. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.HP_ANTIFREE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x43,
                        description=(
                            "Heat pump antifreeze (HP-Antifree) status. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COMPRESSOR_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x50,
                        description=(
                            "Compressor running state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.ODU_FAN_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x51,
                        description=(
                            "Outdoor unit (ODU) fan running state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.FOUR_WAY_VALVE_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x53,
                        description=(
                            "4-way valve state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COMPRESSOR_CRANKCASE_HEATER_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x54,
                        description=(
                            "Compressor crankcase heater state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.UNDERPAN_HEATER_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x55,
                        description=(
                            "Underpan heater state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DEFROSTING_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x56,
                        description=(
                            "Defrosting state. "
                            "Values: 0=End, 1=Defrosting."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.OIL_RETURN_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x57,
                        description=(
                            "Oil return state. "
                            "Values: 0=No oil return, 1=In oil return."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.AMBIENT_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x58,
                        description=(
                            "Ambient temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DEFROST_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x59,
                        description=(
                            "Defrost temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DISCHARGE_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5A,
                        description=(
                            "Discharge temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.SUCTION_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5B,
                        description=(
                            "Suction temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.ODU_FAN_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5C,
                        description=(
                            "Outdoor unit (ODU) fan error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.HIGH_PRESSURE_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5D,
                        description=(
                            "High-pressure sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.HIGH_PRESSURE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5E,
                        description=(
                            "High pressure protection. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.LOW_PRESSURE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x5F,
                        description=(
                            "Low pressure protection. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.HIGH_DISCHARGE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x60,
                        description=(
                            "High discharge protection. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CAPACITY_DIP_SETTING_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x61,
                        description=(
                            "Capacity DIP setting error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COMMUNICATION_ERROR_BETWEEN_IDU_AND_ODU: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x62,
                        description=(
                            "Communication error between IDU and ODU. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.ECONOMIZER_IN_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x63,
                        description=(
                            "Economizer inlet sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.ECONOMIZER_OUT_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x64,
                        description=(
                            "Economizer outlet sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.SYSTEM_RECOVERABLE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x66,
                        description=(
                            "System recoverable protection. "
                            "Values: 0=No, 1=Yes."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.SYSTEM_IRRECOVERABLE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x67,
                        description=(
                            "System irrecoverable protection. "
                            "Values: 0=No, 1=Yes."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.FLOW_SWITCH_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x6C,
                        description=(
                            "Flow switch protection (fault/protection flag related to the water flow proof switch). "
                            "Use: indicates the unit has entered a protection condition due to a flow-switch related issue "
                            "(typically missing/insufficient water circulation); useful to trigger alarms and correlate with pump state. "
                            "Values: 0=Normal, 1=Protected."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DC_BUS_LOW_VOLTAGE_OR_VOLTAGE_DROP: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x80,
                        description=(
                            "DC bus low-voltage or voltage drop. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DC_BUS_OVER_VOLTAGE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x81,
                        description=(
                            "DC bus over-voltage. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.AC_CURRENT_PROTECTION_INPUT_SIDE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x82,
                        description=(
                            "AC current protection (input side). "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IPM_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x83,
                        description=(
                            "IPM error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.PFC_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x84,
                        description=(
                            "PFC error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.STARTUP_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x85,
                        description=(
                            "Startup error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.PHASE_LOSS: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x86,
                        description=(
                            "Phase loss. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DRIVE_MODULE_RESETTING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x87,
                        description=(
                            "Drive module resetting. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COMPRESSOR_OVERCURRENT: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x88,
                        description=(
                            "Compressor overcurrent. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.OVER_SPEED: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x89,
                        description=(
                            "Over-speed. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CHARGING_CIRCUIT_ERROR_OR_CURRENT_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8A,
                        description=(
                            "Charging circuit error or current sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DESYNCHRONIZING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8B,
                        description=(
                            "Desynchronizing. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.COMPRESSOR_STALLING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8C,
                        description=(
                            "Compressor stalling. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DRIVE_COMMUNICATION_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8D,
                        description=(
                            "Drive communication error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.RADIATOR_OR_IPM_OR_PFC_OVER_TEMPERATURE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8E,
                        description=(
                            "Radiator or IPM or PFC over-temperature. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DEFECTIVE_RADIATOR_OR_IPM_OR_PFC: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x8F,
                        description=(
                            "Defective radiator or IPM or PFC. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CHARGING_CIRCUIT_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x92,
                        description=(
                            "Charging circuit error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.AC_INPUT_VOLTAGE_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x93,
                        description=(
                            "AC input voltage error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.DRIVE_BOARD_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x94,
                        description=(
                            "Drive board temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.AC_CONTACTOR_PROTECTION_OR_INPUT_CROSS_ZERO_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x95,
                        description=(
                            "AC contactor protection or input cross-zero error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.TEMP_DRIFT_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x96,
                        description=(
                            "Temperature drift protection. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.SENSOR_CONNECTION_PROTECTION_CONNN: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x97,
                        description=(
                            "Sensor connection protection (connection to phase U or V failed). "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CONDENSER_LEAVING_WATER_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x98,
                        description=(
                            "Condenser leaving water temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.E_HEATER_LEAVING_WATER_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x99,
                        description=(
                            "E-heater leaving water temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.REFRIGERANT_LIQUID_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x9A,
                        description=(
                            "Refrigerant liquid temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CONDENSER_ENTERING_WATER_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x9B,
                        description=(
                            "Condenser entering water temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.WATER_TANK_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x9C,
                        description=(
                            "Water tank temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.REFRIGERANT_VAPOR_LINE_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x9E,
                        description=(
                            "Refrigerant vapor line temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.REMOTE_ROOM_TEMP_SENSOR_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xA0,
                        description=(
                            "Remote room temperature sensor error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.OTHER_HEAT_SOURCE_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xA9,
                        description=(
                            "Other heat source state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.FLOW_SWITCH_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xAA,
                        description=(
                            "Flow switch state (raw input/contact state of the water flow proof switch). "
                            "Use: diagnostics—compare with water pump state and operating request; if Open while circulation is expected, "
                            "check pump, valves, filters, air in circuit, or low water/pressure conditions. "
                            "Values: 0=Close (contact closed), 1=Open (contact open)."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IDU_E_HEATER_1_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xAB,
                        description=(
                            "Indoor unit (IDU) E-heater 1 state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IDU_E_HEATER_2_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xAC,
                        description=(
                            "Indoor unit (IDU) E-heater 2 state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.WATER_TANK_HEATER_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xAD,
                        description=(
                            "Water tank heater state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IDU_WATER_PUMP_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xAF,
                        description=(
                            "Indoor unit (IDU) water pump state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.CIRCULATING_2_WAY_VALVE_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB0,
                        description=(
                            "Circulating 2-way valve state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.PLATE_HEATER_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB1,
                        description=(
                            "Plate heater state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.THREE_WAY_VALVE_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB2,
                        description=(
                            "3-way valve state. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.GATE_CTRL: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB3,
                        description=(
                            "Gate-Ctrl card state. "
                            "Values: 0=Card out, 1=Card in."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.JUMPER_CAP_ERROR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB8,
                        description=(
                            "Jumper cap error. "
                            "Values: 0=Normal, 1=Error."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.E_HEATER_1_WELDING_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xB9,
                        description=(
                            "E-heater 1 welding protection. "
                            "Values: 0=Normal, 1=Protected."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.E_HEATER_2_WELDING_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xBA,
                        description=(
                            "E-heater 2 welding protection. "
                            "Values: 0=Normal, 1=Protected."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.WATER_HEATER_WELDING_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xBB,
                        description=(
                            "Water heater welding protection. "
                            "Values: 0=Normal, 1=Protected."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.WATER_FLOW_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xBC,
                        description=(
                            "Water flow protection (fault/protection flag indicating a water-flow related protection condition). "
                            "Use: alarm flag for BMS/HA—when Yes, the unit may limit/stop operation to protect the hydraulic circuit; "
                            "correlate with Flow Switch State and pump state to diagnose the cause. "
                            "Values: 0=No, 1=Yes."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IDU_RECOVERABLE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xBE,
                        description=(
                            "Indoor unit (IDU) recoverable protection. "
                            "Values: 0=No, 1=Yes."
                        ),
                    ),
                    AermecHMI080BinarySensorFunction.IDU_IRRECOVERABLE_PROTECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0xBF,
                        description=(
                            "Indoor unit (IDU) irrecoverable protection. "
                            "Values: 0=No, 1=Yes."
                        ),
                    ),
                }
            ),
            #
            # SENSOR (Word registers)
            #
            Platform.SENSOR: Register(
                functions={
                    AermecHMI080SensorFunction.UNIT_STATUS: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x00,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        description=(
                            "Unit status (running mode). "
                            "Values: 1=Cool, 2=Heat, 6=Hot water, 8=Off."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_OUTDOOR: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x01,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Outdoor temperature (T-outdoor). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_DISCHARGE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x02,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Discharge temperature (T-discharge). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_DEFROST: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x03,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Defrost temperature (T-defrost). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_SUCTION: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x04,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Suction temperature (T-suction). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_ECONOMIZER_IN: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x05,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Economizer inlet temperature (T-economizer in). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_ECONOMIZER_OUT: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x06,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Economizer outlet temperature (T-economizer out). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.DIS_PRESSURE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x07,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Dis. pressure (as provided by the controller, unit in °C). "
                            "Range: -40..70 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_WATER_OUT_PE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x08,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Leaving water temperature (T-water out PE). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_OPTIONAL_WATER_SENS: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x09,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Optional water sensor temperature (T-optional water sen.). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_WATER_IN_PE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0A,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Entering water temperature (T-water in PE). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_TANK_CTRL: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0B,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Tank control temperature (T-tank ctrl.). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_REMOTE_ROOM: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0C,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Remote room temperature (T-remote room). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_GAS_PIPE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0D,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Gas pipe temperature (T-gas pipe). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_LIQUID_PIPE: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0E,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Liquid pipe temperature (T-liquid pipe). "
                            "Range: -30..150 °C. Transmission value = actual value."
                        ),
                    ),
                    AermecHMI080SensorFunction.THERMOSTAT: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x0F,
                        description=(
                            "Thermostat state. "
                            "Values: 1=Cool, 2=Heat, 3=Off."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_FLOOR_DEBUG: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x10,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Floor debug temperature (calculated value). "
                            "Transmission value = actual calculated value."
                        ),
                    ),
                    AermecHMI080SensorFunction.DEBUG_TIME: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x11,
                        state_class="measurement",
                        unit_of_measurement=UnitOfTime.HOURS,
                        description=(
                            "Debug time (calculated value). "
                            "Unit: hours (h)."
                        ),
                    ),
                    AermecHMI080SensorFunction.DISINFECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x12,
                        description=(
                            "Disinfection status. "
                            "Values: 0=Off, 1=Running, 2=Done, 3=Failed."
                        ),
                    ),
                    AermecHMI080SensorFunction.ERROR_TIME_FOR_FLOOR_DEBUG: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x13,
                        state_class="measurement",
                        unit_of_measurement=UnitOfTime.SECONDS,
                        description=(
                            "Error time for floor debug (calculated value). "
                            "Unit: seconds (s)."
                        ),
                    ),
                    AermecHMI080SensorFunction.T_WEATHER_DEPEND: RegisterFunction(
                        area=RegisterAreaName.AREA_B,
                        address=0x14,
                        function_read=RegisterFunctionRead(precision=1, scale=0.1),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Weather-dependent temperature (calculated value). "
                            "Transmission value = actual calculated value."
                        ),
                    ),
                }
            ),
            #
            # SWITCH (Bit registers + Word 42 on/off)
            #
            Platform.SWITCH: Register(
                functions={
                    AermecHMI080SwitchFunction.DEVICE_POWER_CONTROL: RegisterFunction(
                        area=RegisterAreaName.AREA_C,
                        address=0x2A,
                        description=(
                            "Unit on/off control (Word 42). "
                            "Values: 0xAA=On, 0x55=Off. Default: Off."
                        ),
                    ),
                    AermecHMI080SwitchFunction.WEEKLY_TIMER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x08,
                        description=(
                            "Weekly timer enable. "
                            "Values: 0=Close, 1=Open."
                        ),
                    ),
                    AermecHMI080SwitchFunction.CLOCK_TIMER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x09,
                        description=(
                            "Clock timer enable. "
                            "Values: 0=Close, 1=Open."
                        ),
                    ),
                    AermecHMI080SwitchFunction.TEMP_TIMER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0A,
                        description=(
                            "Temperature timer enable. "
                            "Values: 0=Close, 1=Open."
                        ),
                    ),
                    AermecHMI080SwitchFunction.GATE_CTRL: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x0B,
                        description=(
                            "Gate-Ctrl enable. "
                            "Values: 0=Close, 1=Open."
                        ),
                    ),
                    AermecHMI080SwitchFunction.SOLAR_HEATER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x10,
                        description=(
                            "Solar heater enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.CTRL_STATE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x11,
                        description=(
                            "Control state selection. "
                            "Values: 0=T-water out, 1=T-room."
                        ),
                    ),
                    AermecHMI080SwitchFunction.FAST_HOT_WATER: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x12,
                        description=(
                            "Fast hot water enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.COOL_AND_HOT_WATER_PRIORITY: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x13,
                        description=(
                            "Cool + hot water priority selection. "
                            "Values: 0=Cool, 1=Hot water."
                        ),
                    ),
                    AermecHMI080SwitchFunction.HEAT_AND_HOT_WATER_PRIORITY: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x14,
                        description=(
                            "Heat + hot water priority selection. "
                            "Values: 0=Heat, 1=Hot water."
                        ),
                    ),
                    AermecHMI080SwitchFunction.QUIET_MODE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x15,
                        description=(
                            "Quiet mode enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.WEATHER_DEPEND: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x16,
                        description=(
                            "Weather-dependent control enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.DISINFECTION: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x17,
                        description=(
                            "Disinfection function enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.FLOOR_DEBUG: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x18,
                        description=(
                            "Floor debug enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.FLOOR_DEBUG_START_STOP: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x19,
                        description=(
                            "Floor debug start/stop. "
                            "Values: 0=Stop, 1=Start."
                        ),
                    ),
                    AermecHMI080SwitchFunction.EMERGENCE_MODE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x1A,
                        description=(
                            "Emergency mode enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.OTHER_THERMAL: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x1B,
                        description=(
                            "Other thermal source availability. "
                            "Values: 0=Without, 1=With."
                        ),
                    ),
                    AermecHMI080SwitchFunction.WATER_TANK: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x1D,
                        description=(
                            "Water tank availability. "
                            "Values: 0=Without, 1=With."
                        ),
                    ),
                    AermecHMI080SwitchFunction.SOLAR_SETTING: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x1F,
                        description=(
                            "Solar setting availability. "
                            "Values: 0=Without, 1=With."
                        ),
                    ),
                    AermecHMI080SwitchFunction.REMOTE_SENSOR: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x21,
                        description=(
                            "Remote sensor availability. "
                            "Values: 0=Without, 1=With."
                        ),
                    ),
                    AermecHMI080SwitchFunction.HOLIDAY_MODE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x22,
                        description=(
                            "Holiday mode enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.REFRI_RECOVERY: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x23,
                        description=(
                            "Refri. recovery enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.MANUAL_DEFROST: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x24,
                        description=(
                            "Manual defrost enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                    AermecHMI080SwitchFunction.COOL_2_WAY_VALVE: RegisterFunction(
                        area=RegisterAreaName.AREA_A,
                        address=0x25,
                        description=(
                            "Cool 2-way valve enable. "
                            "Values: 0=Off, 1=On."
                        ),
                    ),
                },
            ),
            #
            # NUMBER (Word registers)
            #
            Platform.NUMBER: Register(
                functions={
                    AermecHMI080NumberFunction.MODE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x02,
                        min=1,
                        max=5,
                        default=1,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Operating mode (Word 2). "
                            "Values: 1=Heat, 2=Hot water, 3=Cool + Heat water, 4=Heat + Hot water, 5=Cool. "
                            "Default: Heat."
                        ),
                    ),
                    AermecHMI080NumberFunction.OPTIONAL_E_HEATER: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x03,
                        min=1,
                        max=3,
                        default=1,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Optional E-heater configuration (Word 3). "
                            "Values: 1=1 set, 2=2 sets, 3=Off. "
                            "Default: 1 set."
                        ),
                    ),
                    AermecHMI080NumberFunction.DISINFECTION_TEMP: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x04,
                        min=40,
                        max=70,
                        default=70,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Disinfection setpoint temperature (Word 4). "
                            "Range: 40..70 °C. Default: 70 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.FLOR_DEBUG_SEGMENTS: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x05,
                        min=1,
                        max=10,
                        default=1,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Floor debug segments (Word 5). "
                            "Range: 1..10 sections. Default: 1 section."
                        ),
                    ),
                    AermecHMI080NumberFunction.FLOR_DEBUG_PERIOD_1_TEMP: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x06,
                        min=25,
                        max=35,
                        default=25,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Floor debug period 1 temperature (Word 6). "
                            "Range: 25..35 °C. Default: 25 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.DELTA_T_OF_SEGMENT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x07,
                        min=2,
                        max=10,
                        default=5,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Delta T of segment (Word 7). "
                            "Range: 2..10 °C. Default: 5 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.SEGMENT_TIME: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x08,
                        min=0,
                        max=72,
                        default=0,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=12,
                        ),
                        description=(
                            "Segment time (Word 8). "
                            "Values: 0=Not set, 12..72=Hours (12-hour steps). Default: 0 hour."
                        ),
                    ),
                    AermecHMI080NumberFunction.WOT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x09,
                        min=7,
                        max=25,
                        default=18,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "WOT-Cool setpoint (Word 9). "
                            "Range: 7..25 °C. Default: 18 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.WOT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0A,
                        min=20,
                        max=55,
                        default=45,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "WOT-Heat setpoint (Word 10). "
                            "Range: 20..60 °C (High-temp units) / 20..55 °C (Low-temp units). "
                            "Default: 45 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.RT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0B,
                        min=18,
                        max=30,
                        default=24,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "RT-Cool setpoint (Word 11). "
                            "Range: 18..30 °C. Default: 24 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.RT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0C,
                        min=18,
                        max=30,
                        default=20,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "RT-Heat setpoint (Word 12). "
                            "Range: 18..30 °C. Default: 20 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.T_WATER_TANK: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0D,
                        min=40,
                        max=80,
                        default=50,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Water tank setpoint temperature (Word 13). "
                            "Range: 40..80 °C. Default: 50 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.T_EHEATER: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0E,
                        min=-20,
                        max=18,
                        default=-15,
                        data_type=DataType.INT16,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Electric heater temperature threshold (T-Eheater, Word 14). "
                            "Range: -20..18 °C. Default: -15 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.T_OTHER_SWITCH_ON: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x0F,
                        min=-20,
                        max=18,
                        default=-20,
                        data_type=DataType.INT16,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Other thermal source switch-on temperature (T-Other switch on, Word 15). "
                            "Range: -20..18 °C. Default: -20 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.T_HP_MAX: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x10,
                        min=40,
                        max=55,
                        default=50,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Heat pump max temperature (T-HP max, Word 16). "
                            "Range: 40..55 °C. Default: 50 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_AT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x11,
                        min=10,
                        max=37,
                        default=25,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper AT-Heat (Word 17). "
                            "Range: 10..37 °C. Default: 25 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_AT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x12,
                        min=-20,
                        max=9,
                        default=-20,
                        data_type=DataType.INT16,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower AT-Heat (Word 18). "
                            "Range: -20..9 °C. Default: -20 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_RT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x13,
                        min=22,
                        max=30,
                        default=24,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper RT-Heat (Word 19). "
                            "Range: 22..30 °C. Default: 24 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_RT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x14,
                        min=18,
                        max=21,
                        default=18,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower RT-Heat (Word 20). "
                            "Range: 18..21 °C. Default: 18 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_WT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x15,
                        min=46,
                        max=60,
                        default=55,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper WT-Heat (Word 21). "
                            "Range: 46..60 °C (High-temp units) / 46..55 °C (Low-temp units). "
                            "Default: 55 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_WT_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x16,
                        min=36,
                        max=45,
                        default=40,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower WT-Heat (Word 22). "
                            "Range: 36..45 °C. Default: 40 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_AT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x17,
                        min=26,
                        max=48,
                        default=40,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper AT-Cool (Word 23). "
                            "Range: 26..48 °C. Default: 40 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_AT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x18,
                        min=10,
                        max=25,
                        default=25,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower AT-Cool (Word 24). "
                            "Range: 10..25 °C. Default: 25 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_RT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x19,
                        min=24,
                        max=30,
                        default=27,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper RT-Cool (Word 25). "
                            "Range: 24..30 °C. Default: 27 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_RT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1A,
                        min=18,
                        max=23,
                        default=22,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower RT-Cool (Word 26). "
                            "Range: 18..23 °C. Default: 22 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.UPPER_WT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1B,
                        min=15,
                        max=25,
                        default=15,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Upper WT-Cool (Word 27). "
                            "Range: 15..25 °C (with FCU). Default: 15 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.LOWER_WT_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1C,
                        min=7,
                        max=14,
                        default=7,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Lower WT-Cool (Word 28). "
                            "Range: 7..14 °C. Default: 7 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.DELTA_T_COOL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1D,
                        min=2,
                        max=10,
                        default=5,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Delta T - Cool (Word 29). "
                            "Range: 2..10 °C. Default: 5 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.DELTA_T_HEAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1E,
                        min=2,
                        max=10,
                        default=10,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Delta T - Heat (Word 30). "
                            "Range: 2..10 °C. Default: 10 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.DELTA_T_HOT_WATER: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x1F,
                        min=2,
                        max=8,
                        default=5,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Delta T - Hot water (Word 31). "
                            "Range: 2..8 °C. Default: 5 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.DELTA_T_ROOM_TEMP: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x20,
                        min=1,
                        max=5,
                        default=2,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        state_class="measurement",
                        device_class="temperature",
                        unit_of_measurement="°C",
                        description=(
                            "Delta T - Room temperature (Word 32). "
                            "Range: 1..5 °C. Default: 2 °C."
                        ),
                    ),
                    AermecHMI080NumberFunction.COOL_RUN_TIME: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x21,
                        min=1,
                        max=10,
                        default=3,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Cool run time (Word 33). "
                            "Range: 1..10 min. Default: 3 min."
                        ),
                    ),
                    AermecHMI080NumberFunction.HEAT_RUN_TIME: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x22,
                        min=1,
                        max=10,
                        default=5,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Heat run time (Word 34). "
                            "Range: 1..10 min. Default: 5 min."
                        ),
                    ),
                    AermecHMI080NumberFunction.OTHER_THERMAL_LOGIC: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x23,
                        min=1,
                        max=3,
                        default=0,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Other thermal logic selection (Word 35). "
                            "Values: 1..3. Default: 1. Disabled: 0."
                        ),
                    ),
                    AermecHMI080NumberFunction.TANK_HEATER: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x24,
                        min=1,
                        max=2,
                        default=0,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Tank heater logic (Word 36). "
                            "Values: 1..2. Default: 1. Disabled: 0."
                        ),
                    ),
                    AermecHMI080NumberFunction.OPTIONAL_E_HEATER_LOGIC: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x25,
                        min=1,
                        max=2,
                        default=0,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Optional E-heater logic (Word 37). "
                            "Values: 1..2. Default: 1. Disabled: 0."
                        ),
                    ),
                    AermecHMI080NumberFunction.CURRENT_LIMIT_VALUE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x26,
                        min=0,
                        max=50,
                        default=16,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Current limit value (Word 38). "
                            "Range: 0..50 A. Default: 16 A."
                        ),
                    ),
                    AermecHMI080NumberFunction.RW_THERMOSTAT: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x27,
                        min=0,
                        max=2,
                        default=0,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Thermostat configuration (Word 39). "
                            "Values: 0=Without, 1=Air, 2=Air + hot water. Default: Without."
                        ),
                    ),
                    AermecHMI080NumberFunction.FORCE_MODE: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x28,
                        min=1,
                        max=3,
                        default=3,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Force mode (Word 40). "
                            "Values: 1=Force-cool, 2=Force-heat, 3=Off. Default: Off."
                        ),
                    ),
                    AermecHMI080NumberFunction.AIR_REMOVAL: RegisterFunction(
                        area=RegisterAreaName.AREA_D,
                        address=0x29,
                        min=1,
                        max=3,
                        function_read=RegisterFunctionRead(precision=0, scale=1),
                        function_write=RegisterFunctionWrite(
                            scale=1,
                            number_mode=NumberMode.BOX,
                            step=1,
                        ),
                        description=(
                            "Air removal selection (Word 41). "
                            "Values: 1=Air, 2=Water tank, 3=Off."
                        ),
                    ),
                },
            ),
        },
    )
