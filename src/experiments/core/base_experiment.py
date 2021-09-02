from __future__ import annotations

from abc import ABC

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from control.core.base_control import BaseControl
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
    from reports.core.base_report import BaseReport
    from simulation.core.base_simulator import BaseSimulator
    from experiments.core.recovery_strategy import RecoveryStrategy


class BaseExperiment(ABC):
    """Simulation experiment"""

    __dynamic_system: BaseDynamicSystem
    """Dynamic system where things will be built"""

    __simulator: BaseSimulator
    """Dynamic system where things will be built"""

    __control: BaseControl
    """Control for the simulation"""

    __report: BaseReport
    """Report module for the simulation"""

    __recovery_strategy: RecoveryStrategy
    """Strategy for persistence of the experiment"""

    def __init__(
        self,
        dynamic_system: BaseDynamicSystem,
        simulator: BaseSimulator,
        control: BaseControl,
        report: BaseReport,
        recovery_strategy: RecoveryStrategy,
    ):
        self.__dynamic_system = dynamic_system
        self.__simulator = simulator
        self.__control = control
        self.__report = report
        self.__recovery_strategy = recovery_strategy

    @property
    def dynamic_system(self) -> BaseDynamicSystem:
        """Gets the dynamic system of the experiment"""
        return self.__dynamic_system

    @property
    def simulator(self) -> BaseSimulator:
        """Gets the simulator of the experiment"""
        return self.__simulator

    @property
    def simulation_control(self) -> BaseControl:
        """Gets the simulation control of the experiment"""
        return self.__control

    @property
    def simulation_report(self) -> BaseReport:
        """Gets the simulation report of the experiment"""
        return self.__report

    def save(self):
        self.__control.stop()
        return self.__recovery_strategy.save(self)

    def load(self, data: Any):
        return self.__recovery_strategy.load(data)
