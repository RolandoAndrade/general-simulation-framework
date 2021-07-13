from __future__ import annotations

from control.controls.discrete_event_control import DiscreteEventControl
from control.core.base_control import BaseControl
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.core.base_experiment import BaseExperiment
from reports.core.base_report import BaseReport
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines.discrete_event_simulation_engine import DiscreteEventSimulationEngine


class DiscreteEventExperiment(BaseExperiment):
    """Discrete-event simulation experiment"""

    def __init__(self,
                 dynamic_system: DiscreteEventDynamicSystem,
                 simulator: DiscreteEventSimulationEngine = None,
                 control: BaseControl = None,
                 report: BaseReport = None):
        report = report or DefaultReport()
        simulator = simulator or DiscreteEventSimulationEngine(dynamic_system, report)
        control = control or DiscreteEventControl(simulator)
        super(DiscreteEventExperiment, self).__init__(dynamic_system, simulator, control, report)