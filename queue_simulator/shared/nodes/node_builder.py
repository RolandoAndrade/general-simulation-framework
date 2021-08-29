from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.shared.nodes.node_types import NodeType
from queue_simulator.source import Source

expected_nodes = {
    NodeType.SOURCE: Source,
}


class NodeBuilder:
    @staticmethod
    def create_node(node_type: NodeType, dynamic_system: DiscreteEventDynamicSystem):
        return expected_nodes[node_type](dynamic_system)
