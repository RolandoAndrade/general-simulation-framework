from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.queue_components.entities import NameGenerator, Emitter
from queue_simulator.queue_components.server import Server
from queue_simulator.queue_components.shared.nodes.node_types import NodeType
from queue_simulator.queue_components.sink.sink import Sink
from queue_simulator.queue_components.source import Source, GraphicSource

expected_nodes = {
    NodeType.SOURCE: GraphicSource,
    NodeType.SERVER: Server,
    NodeType.SINK: Sink,
    NodeType.ENTITY_EMITTER: Emitter,
}


class NodeBuilder:
    @staticmethod
    def create_node(
        node_type: NodeType,
        dynamic_system: DiscreteEventDynamicSystem,
        entity_manager: NameGenerator,
    ):
        if node_type == NodeType.ENTITY_EMITTER:
            return expected_nodes[node_type](
                entity_manager.get_name(node_type), entity_manager
            )
        return expected_nodes[node_type](
            dynamic_system,
            entity_manager.get_name(node_type),
            entity_manager=entity_manager,
        )
