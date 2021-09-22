from typing import Any

from queue_simulator.queue_components.shared.units.unit_conversion import UnitConversion


class TimeConversion(UnitConversion):
    units = {
        "Seconds": 1,
        "Minutes": 1 * 60,
        "Hours": 1 * 60 * 60,
        "Days": 1 * 60 * 60 * 24
    }

    def convert(self, value: Any, from_unit: str, to_unit: str = "Milliseconds"):
        return value * self.units[from_unit]