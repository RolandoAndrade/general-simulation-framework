from core.events import EventBus
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.queue_components.entities import NameGenerator, GraphicEmitter
from queue_simulator.queue_components.server import GraphicServer
from queue_simulator.queue_components.shared.nodes.node_types import NodeType
from queue_simulator.queue_components.sink import GraphicSink
from queue_simulator.queue_components.source import GraphicSource

expected_nodes = {
    NodeType.SOURCE: GraphicSource,
    NodeType.SERVER: GraphicServer,
    NodeType.SINK: GraphicSink,
    NodeType.ENTITY_EMITTER: GraphicEmitter,
}


class NodeBuilder:
    @staticmethod
    def create_node(
        node_type: NodeType,
        dynamic_system: DiscreteEventDynamicSystem,
        entity_manager: NameGenerator,
        event_bus: EventBus
    ):
        if node_type == NodeType.ENTITY_EMITTER:
            return expected_nodes[node_type](
                entity_manager.get_name(node_type), entity_manager
            )
        return expected_nodes[node_type](
            dynamic_system,
            entity_manager.get_name(node_type),
            entity_manager=entity_manager,
            event_bus=event_bus
        )
