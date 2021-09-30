"""Base Experiment
===================
This module contains the abstract definition of an experiment.
It has an abstract definition BaseExperiment that should be extended
using the concrete classes of the simulation paradigm to be used.

Example:
    Creating an experiment::

        class DiscreteEventExperiment(BaseExperiment):
            def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
                report = DefaultReport()
                simulator = DiscreteEventSimulationEngine(dynamic_system, report)
                control = DiscreteEventControl(simulator, ThreadControlStrategy())
                recovery_strategy = PickleRecovery()
                super(DiscreteEventExperiment, self).__init__(
                    dynamic_system, simulator, control, report, recovery_strategy
                )
"""

from __future__ import annotations

from abc import ABC

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gsf.control.core.base_control import BaseControl
    from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
    from gsf.reports.core.base_report import BaseReport
    from gsf.simulation.core.base_simulator import BaseSimulator
    from gsf.experiments.core.recovery_strategy import RecoveryStrategy


class BaseExperiment(ABC):
    """Simulation experiment

    Organizes the simulation modules.

    Attributes:
        __dynamic_system (BaseDynamicSystem): Dynamic system where things will be built.
        __simulator (BaseSimulator): Simulator that will run the simulations.
        __control (BaseControl): Control for the simulation.
        __report (BaseReport): Report module for the simulation.
        __recovery_strategy (RecoveryStrategy): Strategy for persistence of the experiment.
    """

    __dynamic_system: BaseDynamicSystem
    """Dynamic system where things will be built."""

    __simulator: BaseSimulator
    """Simulator that will run the simulations."""

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
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system where things will be built.
            simulator (BaseSimulator): Simulator that will run the simulations.
            control (BaseControl): Control for the simulation.
            report (BaseReport): Report module for the simulation.
            recovery_strategy (RecoveryStrategy): Strategy for persistence of the experiment.
        """
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
        """Saves the experiment."""
        self.__control.stop()
        return self.__recovery_strategy.save(self)

    def load(self, data: Any):
        """Imports an already existing experiment."""
        return self.__recovery_strategy.load(data)
