from __future__ import annotations

from typing import Set, List

from control.controls import ThreadControlStrategy
from control.controls.discrete_event_control import DiscreteEventControl
from control.core import SimulationStats
from core.events import EventBus, DomainEvents
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.queue_components.entities import NameGenerator, Emitter, AvailableEntities
from queue_simulator.queue_components.label.graph_label import GraphLabel
from queue_simulator.queue_components.route.route import Route
from queue_simulator.queue_components.dynamic_systems import SimulationDynamicSystem
from queue_simulator.queue_components.shared.expressions import ExpressionManager
from queue_simulator.queue_components.shared.graphic import Point2D
from queue_simulator.queue_components.shared.models.node_property import NodeProperty
from queue_simulator.queue_components.shared.nodes import NodeBuilder, NodeType
from queue_simulator.queue_components.shared.stats import ComponentStats
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines import DiscreteEventSimulationEngine


class SimulationExperiment(DiscreteEventExperiment):
    _event_bus: EventBus

    _name_generator: NameGenerator

    dynamic_system: SimulationDynamicSystem
    simulation_control: DiscreteEventControl
    simulator: DiscreteEventSimulationEngine

    _emitters: Set[Emitter]

    _labels: Set[GraphLabel]

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
        self._labels = set()
        self._expression_manager = ExpressionManager()

    def add_node(self, node_type: NodeType):
        node = NodeBuilder.create_node(
            node_type, self.dynamic_system, self._name_generator, self.event_bus
        )
        if node_type == NodeType.ENTITY_EMITTER:
            self._emitters.add(node)
        self._expression_manager.add_expression(node.get_id(), node.get_expressions())
        return node

    def add_label(self):
        label = GraphLabel(self._name_generator.get_name(AvailableEntities.LABEL),
                           self._name_generator, self._expression_manager)
        self._labels.add(label)
        return label

    def edit_label(self, component: str, new_property: NodeProperty):
        label = self._get_label(component)
        if label is not None:
            if new_property.property_name == "Name":
                label.set_id(new_property.property_name)
            else:
                label.set_expression(new_property.property_value)
        return label

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

    def _get_label(self, name: str):
        for label in self._labels:
            if label.get_id() == name:
                return label
        return None

    def _remove_model(self, component: str) -> bool:
        model = self.dynamic_system.get_model(component)
        if model is not None:
            self._expression_manager.remove_expression(model.get_id())
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
            self._expression_manager.remove_expression(emitter.get_id())
            self._emitters.remove(emitter)
            return True
        return False

    def _remove_label(self, component: str) -> bool:
        label = self._get_label(component)
        if label is not None:
            self._labels.remove(label)
            return True
        return False

    def remove_component(self, component: str):
        return (
                self._remove_model(component)
                or self._remove_path(component)
                or self._remove_emitter(component)
                or self._remove_label(component)
        )

    def edit_property(self, component: str, new_property: NodeProperty):
        with_expression = self.dynamic_system.get_model(component) or self._get_emitter(component)
        node = (
                self.dynamic_system.get_model(component)
                or self.dynamic_system.get_path(component)
                or self._get_emitter(component)
        )
        if node is not None:
            last_id = node.get_id()
            node.set_serialized_property(new_property, self._expression_manager)
            if with_expression is not None:
                self._expression_manager.remove_expression(last_id)
                self._expression_manager.add_expression(node.get_id(), node.get_expressions())
        return node

    @property
    def event_bus(self):
        return self._event_bus

    def get_expressions(self):
        return self._expression_manager.get_available_expressions()

    def start_simulation(
            self, stop_time: Time, step: Time = None, wait_time: Time = None, init: bool = True
    ):
        if init:
            self.dynamic_system.init()
        if step is not None:
            step = Time(step)
        self.simulation_control.start(
            None, step or Time(1000), stop_time, wait_time or 0
        )

    def next_step(
            self, stop_time: Time = None, step: Time = None,
            init: bool = True
    ):
        if init:
            self.dynamic_system.init()
        if 0 <= self.simulation_control.time + self.simulator.get_time_of_next_event() <= stop_time:
            time = self.simulation_control.next_step()
            self.event_bus.emit(DomainEvents.SIMULATION_STATUS,
                                SimulationStats(time, stop_time, step, True),)
            if time >= stop_time:
                self.simulation_control.stop()
                self.event_bus.emit(DomainEvents.SIMULATION_FINISHED)

    def get_stats(self) -> List[ComponentStats]:
        return self.dynamic_system.get_stats()

    def move_node(self, component: str, position: Point2D):
        node = self.dynamic_system.get_model(component)
        node.set_position(position)
        return node
