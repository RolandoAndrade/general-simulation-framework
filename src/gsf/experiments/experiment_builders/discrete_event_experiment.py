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
    """Discrete-event simulation experiment"""

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        simulator: DiscreteEventSimulationEngine = None,
        control: BaseControl = None,
        report: BaseReport = None,
        recovery_strategy: RecoveryStrategy = None,
    ):
        report = report or DefaultReport()
        simulator = simulator or DiscreteEventSimulationEngine(dynamic_system, report)
        control = control or DiscreteEventControl(simulator, ThreadControlStrategy())
        recovery_strategy = recovery_strategy or PickleRecovery()
        super(DiscreteEventExperiment, self).__init__(
            dynamic_system, simulator, control, report, recovery_strategy
        )
