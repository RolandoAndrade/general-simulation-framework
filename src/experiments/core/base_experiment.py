from __future__ import annotations

from abc import ABC

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from control.core.base_control import BaseControl
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
    from reports.core.base_report import BaseReport
    from simulation.core.base_simulator import BaseSimulator


class BaseExperiment(ABC):
    """Simulation experiment"""

    __dynamicSystem: BaseDynamicSystem
    """Dynamic system where things will be built"""

    __simulator: BaseSimulator
    """Dynamic system where things will be built"""

    __control: BaseControl
    """Control for the simulation"""

    __report: BaseReport
    """Report module for the simulation"""

    def __init__(self,
                 dynamic_system: BaseDynamicSystem,
                 simulator: BaseSimulator,
                 control: BaseControl,
                 report: BaseReport):
        self.__dynamicSystem = dynamic_system
        self.__simulator = simulator
        self.__control = control
        self.__report = report

    def dynamicSystem(self) -> BaseDynamicSystem:
        """Gets the dynamic system of the experiment"""
        return self.__dynamicSystem

    def simulator(self) -> BaseSimulator:
        """Gets the simulator of the experiment"""
        return self.__simulator

    def simulationControl(self) -> BaseControl:
        """Gets the simulation control of the experiment"""
        return self.__control

    def simulationReport(self) -> BaseReport:
        """Gets the simulation report of the experiment"""
        return self.__report
