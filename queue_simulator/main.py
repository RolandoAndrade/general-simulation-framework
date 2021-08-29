from typing import List, Dict

import eventlet
import socketio

from loguru import logger
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.shared.dynamic_systems import SimulationDynamicSystem
from queue_simulator.shared.experiments.simulation_experiment import SimulationExperiment
from queue_simulator.shared.nodes import NodeType, NodeBuilder

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
        session['experiment'] = SimulationExperiment()


@sio.event
def create_node(sid, data: Dict[str, NodeType]):
    node = data['node']
    logger.info("Create node: {node}, sid: {sid}", node=node, sid=sid)
    session: Dict[str, SimulationExperiment]
    with sio.session(sid) as session:
        created_node = session['experiment'].add_node(node)
    return created_node.serialize()

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 4000)), app)
