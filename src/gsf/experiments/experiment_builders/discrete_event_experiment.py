"""Discrete Event Experiment
=============================
This module contains the definition of a discrete-event experiment.
It has the definition of the DiscreteEventExperiment that allows to create discrete-event
experiments and simulate them.

Example:
    Creating a discrete-event experiment::

        dynamic_system = some_discrete_event_dynamic_system
        simulator = DiscreteEventExperiment(dynamic_system)
"""

from __future__ import annotations

from gsf.control.controls import ThreadControlStrategy
from gsf.control.controls.discrete_event_control import DiscreteEventControl
from gsf.control.core.base_control import BaseControl
from gsf.dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from gsf.experiments.core.recovery_strategy import RecoveryStrategy
from gsf.experiments.core.base_experiment import BaseExperiment
from gsf.experiments.strategies.pickle_recovery import PickleRecovery
from gsf.reports.core.base_report import BaseReport
from gsf.reports.report_generators.default_report import DefaultReport
from gsf.simulation.simulation_engines.discrete_event_simulation_engine import (
    DiscreteEventSimulationEngine,
)


class DiscreteEventExperiment(BaseExperiment):
    """Discrete-event simulation experiment

    If the module's instances are not given, it creates a discrete-event compatible module.
    """

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        simulator: DiscreteEventSimulationEngine = None,
        control: BaseControl = None,
        report: BaseReport = None,
        recovery_strategy: RecoveryStrategy = None,
    ):
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system where things will be built.
            simulator (BaseSimulator): Simulator that will run the simulations.
            control (BaseControl): Control for the simulation.
            report (BaseReport): Report module for the simulation.
            recovery_strategy (RecoveryStrategy): Strategy for persistence of the experiment.
        """
        report = report or DefaultReport()
        simulator = simulator or DiscreteEventSimulationEngine(dynamic_system, report)
        control = control or DiscreteEventControl(simulator, ThreadControlStrategy())
        recovery_strategy = recovery_strategy or PickleRecovery()
        super(DiscreteEventExperiment, self).__init__(
            dynamic_system, simulator, control, report, recovery_strategy
        )
