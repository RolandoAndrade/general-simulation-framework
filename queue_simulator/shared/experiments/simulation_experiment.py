from control.controls.discrete_event_control import DiscreteEventControl
from core.entity.properties import ExpressionProperty
from core.events import EventBus
from core.mathematics.values.value import Value
from experiments.experiment_builders import DiscreteEventExperiment
from models.core import Path
from queue_simulator.entities import NameGenerator
from queue_simulator.route.route import Route
from queue_simulator.shared.dynamic_systems import SimulationDynamicSystem
from queue_simulator.shared.nodes import NodeBuilder, NodeType
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines import DiscreteEventSimulationEngine


class SimulationExperiment(DiscreteEventExperiment):
    _event_bus: EventBus

    _name_generator: NameGenerator

    dynamic_system: SimulationDynamicSystem

    def __init__(self):
        eb = EventBus()
        dynamic_system = SimulationDynamicSystem()
        report = DefaultReport(eb)
        simulator = DiscreteEventSimulationEngine(dynamic_system, report)
        control = DiscreteEventControl(simulator, eb)
        super().__init__(dynamic_system, simulator, control, report)

        self._name_generator = NameGenerator()
        self._event_bus = eb

    def add_node(self, node_type: NodeType):
        return NodeBuilder.create_node(node_type, self.dynamic_system, self._name_generator)

    def add_path(self, from_node: str, to_node: str):
        from_model = self.dynamic_system.get_model(from_node)
        to_model = self.dynamic_system.get_model(to_node)
        created_path = Route(from_model, to_model, self._name_generator)
        self.dynamic_system.link(created_path)
        return created_path

    @property
    def event_bus(self):
        return self._event_bus
