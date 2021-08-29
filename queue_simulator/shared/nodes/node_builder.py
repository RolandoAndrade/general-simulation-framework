from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.entities import Emitter, NameGenerator
from queue_simulator.server.server import Server
from queue_simulator.shared.nodes.node_types import NodeType
from queue_simulator.sink.sink import Sink
from queue_simulator.source import Source

expected_nodes = {
    NodeType.SOURCE: Source,
    NodeType.SERVER: Server,
    NodeType.SINK: Sink,
    NodeType.ENTITY_EMITTER: Emitter
}


class NodeBuilder:
    @staticmethod
    def create_node(node_type: NodeType, dynamic_system: DiscreteEventDynamicSystem, entity_manager: NameGenerator):
        return expected_nodes[node_type](dynamic_system,
                                         entity_manager.get_name(node_type), entity_manager=entity_manager)
