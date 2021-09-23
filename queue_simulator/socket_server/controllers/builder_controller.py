import json
from typing import Dict, Any

import jsonpickle
from loguru import logger

from queue_simulator.queue_components.experiments import SimulationExperiment
from queue_simulator.queue_components.shared.models.node_property import NodeProperty
from queue_simulator.queue_components.shared.nodes import NodeType
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
    def create_label(sid, data: Dict[str, NodeType]):
        node = data["node"]
        logger.info("Create label: {node}, sid: {sid}", node=node, sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_node = session["experiment"].add_label()
        return created_node.serialize()

    @staticmethod
    @sio.event
    def edit_label(sid, data: Dict[str, Any]):
        component = data["component"]
        new_property = NodeProperty.deserialize(data["property"])
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session["experiment"].edit_label(component, new_property)
        return created_path.serialize()

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

    @staticmethod
    @sio.event
    def get_expressions(sid, data: Dict[str, Any]):
        logger.info("Getting available expressions, sid:{sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            expressions = session["experiment"].get_expressions()
        return {
            'data': jsonpickle.dumps(expressions)
        }

    @staticmethod
    @sio.event
    def save_experiment(sid, data):
        logger.info("Saving experiment, sid:{sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            saved_data = session["experiment"].save()
        return {"data": saved_data}

    @staticmethod
    @sio.event
    def load_experiment(sid, data: Dict[str, Any]):
        logger.info("Load experiment, sid:{sid}", sid=sid)
        experiment = data["experiment"]
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            recovered = session["experiment"].load(experiment)
            session["experiment"] = recovered
        return recovered.dynamic_system.serialize()

    @staticmethod
    @sio.event
    def move_node(sid, data: Dict[str, Any]):
        component = data['component']
        position = data['position']
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            node = session["experiment"].move_node(component, position)
        return node.serialize()
