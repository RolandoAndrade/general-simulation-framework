from __future__ import annotations

import enum
from typing import cast


class TimeUnit(enum.Enum):
    MILLISECOND = "millisecond"
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "moth"
    YEAR = "year"


class SimulationTime:
    __time: int
    """Value of the time"""

    __unit: TimeUnit
    """Unit of time"""

    def __init__(self, time: int, unit: TimeUnit):
        self.__unit = unit
        self.__time = SimulationTime.to_millis(time, unit)

    @staticmethod
    def to_millis(time: int, unit: TimeUnit) -> int:
        unit_conversion = {
            TimeUnit.MILLISECOND: 1,
            TimeUnit.SECOND: 1000,
            TimeUnit.MINUTE: 1000 * 60,
            TimeUnit.HOUR: 1000 * 60 * 60,
            TimeUnit.DAY: 1000 * 60 * 60 * 24,
            TimeUnit.WEEK: 1000 * 60 * 60 * 24 * 7,
            TimeUnit.MONTH: 1000 * 60 * 60 * 24 * 30,
            TimeUnit.YEAR: 1000 * 60 * 60 * 24 * 365
        }
        return time * unit_conversion[unit]

    def __to_unit(self) -> int:
        return self.to_unit(self.__unit)

    def to_unit(self, new_unit: TimeUnit) -> int:
        unit_conversion = {
            TimeUnit.MILLISECOND: 1,
            TimeUnit.SECOND: 1000,
            TimeUnit.MINUTE: 1000 * 60,
            TimeUnit.HOUR: 1000 * 60 * 60,
            TimeUnit.DAY: 1000 * 60 * 60 * 24,
            TimeUnit.WEEK: 1000 * 60 * 60 * 24 * 7,
            TimeUnit.MONTH: 1000 * 60 * 60 * 24 * 30,
            TimeUnit.YEAR: 1000 * 60 * 60 * 24 * 365
        }
        return cast(int, self.__time / unit_conversion[new_unit])

    @property
    def time(self) -> int:
        return self.__to_unit()

    @time.setter
    def time(self, time: int):
        self.__time = SimulationTime.to_millis(time, self.__unit)

    @property
    def millis(self) -> int:
        return self.__time

    def __validate_units(self, other: SimulationTime):
        if self.__unit != other.__unit:
            raise Exception("Units do not equal: " + str(self.__unit) + " != " + str(other.__unit))

    def __add__(self, other: SimulationTime) -> SimulationTime:
        self.__validate_units(other)
        return SimulationTime(self.time + other.time, self.__unit)

    def __sub__(self, other: SimulationTime) -> SimulationTime:
        self.__validate_units(other)
        return SimulationTime(self.time - other.time, self.__unit)
