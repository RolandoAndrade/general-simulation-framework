from typing import Any, cast

from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.entities import NameGenerator
from queue_simulator.shared.dynamic_systems import SimulationDynamicSystem
from queue_simulator.shared.nodes import NodeBuilder, NodeType


class SimulationExperiment(DiscreteEventExperiment):
    _name_generator: NameGenerator

    dynamic_system: SimulationDynamicSystem

    def __init__(self):
        super().__init__(SimulationDynamicSystem())
        self._name_generator = NameGenerator()

    def add_node(self, node_type: NodeType):
        return NodeBuilder.create_node(node_type, self.dynamic_system, self._name_generator.get_name(cast(Any, node_type)))
