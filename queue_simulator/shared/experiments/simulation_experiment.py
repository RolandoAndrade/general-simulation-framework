from __future__ import annotations

from typing import Set, List

from control.controls import ThreadControlStrategy
from control.controls.discrete_event_control import DiscreteEventControl
from core.events import EventBus
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.entities import NameGenerator, Emitter
from queue_simulator.route.route import Route
from queue_simulator.shared.dynamic_systems import SimulationDynamicSystem
from queue_simulator.shared.expressions import ExpressionManager
from queue_simulator.shared.models.node_property import NodeProperty
from queue_simulator.shared.nodes import NodeBuilder, NodeType
from queue_simulator.shared.stats import ComponentStats
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines import DiscreteEventSimulationEngine


class SimulationExperiment(DiscreteEventExperiment):
    _event_bus: EventBus

    _name_generator: NameGenerator

    dynamic_system: SimulationDynamicSystem

    _emitters: Set[Emitter]

    _expression_manager: ExpressionManager

    def __init__(self):
        eb = EventBus()
        dynamic_system = SimulationDynamicSystem()
        report = DefaultReport(eb)
        simulator = DiscreteEventSimulationEngine(dynamic_system, report)
        control = DiscreteEventControl(simulator, ThreadControlStrategy(), eb)
        super().__init__(dynamic_system, simulator, control, report)

        self._name_generator = NameGenerator()
        self._event_bus = eb
        self._emitters = set()
        self._expression_manager = ExpressionManager()

    def add_node(self, node_type: NodeType):
        node = NodeBuilder.create_node(
            node_type, self.dynamic_system, self._name_generator
        )
        if node_type == NodeType.ENTITY_EMITTER:
            self._emitters.add(node)
        self._expression_manager.add_expression(node.get_id(), node.get_expressions())
        return node

    def add_path(self, from_node: str, to_node: str):
        from_model = self.dynamic_system.get_model(from_node)
        to_model = self.dynamic_system.get_model(to_node)
        created_path = Route(from_model, to_model, self._name_generator)
        self.dynamic_system.link(created_path)
        return created_path

    def _get_emitter(self, name: str):
        for emitter in self._emitters:
            if emitter.get_id() == name:
                return emitter
        return None

    def _remove_model(self, component: str) -> bool:
        model = self.dynamic_system.get_model(component)
        if model is not None:
            model.remove()
            return True
        return False

    def _remove_path(self, component: str) -> bool:
        path = self.dynamic_system.get_path(component)
        if path is not None:
            self.dynamic_system.unlink(path)
            return True
        return False

    def _remove_emitter(self, component: str) -> bool:
        emitter = self._get_emitter(component)
        if emitter is not None:
            self._emitters.remove(emitter)
            return True
        return False

    def remove_component(self, component: str):
        return (
                self._remove_model(component)
                or self._remove_path(component)
                or self._remove_emitter(component)
        )

    def edit_property(self, component: str, new_property: NodeProperty):
        node = (
                self.dynamic_system.get_model(component)
                or self.dynamic_system.get_path(component)
                or self._get_emitter(component)
        )
        if node is not None:
            node.set_serialized_property(new_property)
        return node

    @property
    def event_bus(self):
        return self._event_bus

    def start_simulation(self, stop_time: Time, step: Time = None, wait_time: Time = None):
        self.dynamic_system.init()
        self.simulation_control.start(None, step or Time(1000), stop_time, wait_time or Time(0))

    def get_stats(self) -> List[ComponentStats]:
        return self.dynamic_system.get_stats()
