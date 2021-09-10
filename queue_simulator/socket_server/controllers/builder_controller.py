from typing import Dict, Any

from loguru import logger

from queue_simulator.shared.experiments import SimulationExperiment
from queue_simulator.shared.models.node_property import NodeProperty
from queue_simulator.shared.nodes import NodeType
from queue_simulator.socket_server.socket_server import sio


class BuilderController:
    @staticmethod
    @sio.event
    def create_node(sid, data: Dict[str, NodeType]):
        node = data["node"]
        logger.info("Create node: {node}, sid: {sid}", node=node, sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_node = session["experiment"].add_node(node)
        return created_node.serialize()

    @staticmethod
    @sio.event
    def create_path(sid, data: Dict[str, str]):
        from_node = data["from"]
        to_node = data["to"]
        logger.info(
            "Create path from {from_node} to {to_node}, sid: {sid}",
            from_node=from_node,
            to_node=to_node,
            sid=sid,
        )
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session["experiment"].add_path(from_node, to_node)
        return created_path.serialize()

    @staticmethod
    @sio.event
    def remove_component(sid, data: Dict[str, str]):
        component = data["component"]
        logger.info(
            "Remove component {component}, sid: {sid}",
            component=component,
            sid=sid,
        )
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            removed = session["experiment"].remove_component(component)
        return removed

    @staticmethod
    @sio.event
    def edit_property(sid, data: Dict[str, Any]):
        component = data["component"]
        new_property = NodeProperty.deserialize(data["property"])
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session["experiment"].edit_property(component, new_property)
        return created_path.serialize()
