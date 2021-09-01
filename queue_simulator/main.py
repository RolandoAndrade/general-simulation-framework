from typing import List, Dict

import eventlet
import socketio

from loguru import logger

from queue_simulator.shared.experiments import SimulationSocketExperiment
from queue_simulator.shared.experiments.simulation_experiment import SimulationExperiment
from queue_simulator.shared.nodes import NodeType

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

serial = 0


@sio.event
def connect(sid, environ):
    logger.info("Client connected: {sid}", sid=sid)
    session: Dict[str, SimulationExperiment]
    with sio.session(sid) as session:
        session['experiment'] = SimulationSocketExperiment(sio, sid)


@sio.event
def create_node(sid, data: Dict[str, NodeType]):
    node = data['node']
    logger.info("Create node: {node}, sid: {sid}", node=node, sid=sid)
    session: Dict[str, SimulationExperiment]
    with sio.session(sid) as session:
        created_node = session['experiment'].add_node(node)
    return created_node.serialize()


@sio.event
def create_path(sid, data: Dict[str, str]):
    from_node = data['from']
    to_node = data['to']
    logger.info("Create path from {from_node} to {to_node}, sid: {sid}", from_node=from_node, to_node=to_node, sid=sid)
    session: Dict[str, SimulationExperiment]
    with sio.session(sid) as session:
        created_path = session['experiment'].add_path(from_node, to_node)
    return created_path.serialize()


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 4000)), app)
