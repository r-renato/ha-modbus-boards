


class SDM120(SDM):

    def __init__(self, *args, **kwargs):
        self.model = "SDM120"
        self.baud = 2400

        super().__init__(*args, **kwargs)

        self.registers = {
            "voltage": (0x0000, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Voltage", "V", 1, 1),
            "current": (0x0006, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Current", "A", 1, 1),
            "power_active": (0x000c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Active)", "W", 1, 1),
            "power_apparent": (0x0012, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Apparent)", "VA", 1, 1),
            "power_reactive": (0x0018, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power (Reactive)", "VAr", 1, 1),
            "power_factor": (0x001e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Power Factor", "", 1, 1),
            "phase_angle": (0x0024, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Phase Angle", "°", 1, 1),
            "frequency": (0x0046, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Frequency", "Hz", 1, 1),
            "import_energy_active": (0x0048, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Active)", "kWh", 1, 1),
            "export_energy_active": (0x004a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Active)", "kWh", 1, 1),
            "import_energy_reactive": (0x004c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Imported Energy (Reactive)", "kVArh", 1, 1),
            "export_energy_reactive": (0x004e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Exported Energy (Reactive)", "kVArh", 1, 1),
            "total_demand_power_active": (0x0054, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Power (Active)", "W", 2, 1),
            "maximum_total_demand_power_active": (0x0056, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Power (Active)", "W", 2, 1),
            "import_demand_power_active": (0x0058, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Import Demand Power (Active)", "W", 2, 1),
            "maximum_import_demand_power_active": (0x005a, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Import Demand Power (Active)", "W", 2, 1),
            "export_demand_power_active": (0x005c, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Export Demand Power (Active)", "W", 2, 1),
            "maximum_export_demand_power_active": (0x005e, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Export Demand Power (Active)", "W", 2, 1),
            "total_demand_current": (0x0102, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Demand Current", "A", 3, 1),
            "maximum_total_demand_current": (0x0108, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Maximum Total Demand Current", "A", 3, 1),
            "total_energy_active": (0x0156, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Active)", "kWh", 4, 1),
            "total_energy_reactive": (0x0158, 2, meter.registerType.INPUT, meter.registerDataType.FLOAT32, float, "Total Energy (Reactive)", "kVArh", 4, 1),

            "demand_time": (0x0000, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Time", "s", 1, 1),
            "demand_period": (0x0002, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Demand Period", "s", 1, 1),
            "relay_pulse_width": (0x000c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Relay Pulse Width", "ms", 1, 1),
            "network_parity_stop": (0x0012, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Network Parity Stop", [
                "N-1", "E-1", "O-1", "N-2"], 1, 1),
            "meter_id": (0x0014, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Meter ID", "", 1, 1),
            "baud": (0x001c, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Baud Rate", [
                2400, 4800, 9600, -1, -1, 1200], 1, 1),
            "p1_output_mode": (0x0056, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Output Mode", [
                0x0, "Import Energy (Active)", "Import + Export Energy (Active)", 0x3, "Export Energy (Active)",
                "Import Energy (Reactive)", "Import + Export Energy (Reactive)", 0x7, "Export Energy (Reactive)"], 2, 1),
            "display_scroll_timing": (0xf900, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Display Scroll Timing", "s", 3, 1),
            "p1_divisor": (0xf910, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "P1 Divisor", [
                "0.001kWh/imp", "0.01kWh/imp", "0.1kWh/imp", "1kWh/imp"], 3, 1),
            "measurement_mode": (0xf920, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Measurement Mode", [
                0x0, "Total Imported", "Total Imported + Exported", "Total Imported - Exported"], 3, 1),
            "indicator_mode": (0xf930, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Pulse/LED Indicator Mode", [
                "Import + Export Energy (Active)", "Import Energy (Active)", "Export Energy (Active)"], 3, 1),
            "serial_number": (0xfc00, 2, meter.registerType.HOLDING, meter.registerDataType.UINT32, int, "Serial Number", "", 4, 1),
            "software_version": (0xfc03, 2, meter.registerType.HOLDING, meter.registerDataType.FLOAT32, int, "Software Version", "", 4, 1)
        }