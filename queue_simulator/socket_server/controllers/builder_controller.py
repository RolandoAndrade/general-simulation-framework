from typing import Dict

from loguru import logger

from queue_simulator.shared.experiments import SimulationExperiment
from queue_simulator.shared.nodes import NodeType
from queue_simulator.socket_server.socket_server import sio


class BuilderController:
    @staticmethod
    @sio.event
    def create_node(sid, data: Dict[str, NodeType]):
        node = data['node']
        logger.info("Create node: {node}, sid: {sid}", node=node, sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_node = session['experiment'].add_node(node)
        return created_node.serialize()

    @staticmethod
    @sio.event
    def create_path(sid, data: Dict[str, str]):
        from_node = data['from']
        to_node = data['to']
        logger.info("Create path from {from_node} to {to_node}, sid: {sid}", from_node=from_node, to_node=to_node,
                    sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session['experiment'].add_path(from_node, to_node)
        return created_path.serialize()
