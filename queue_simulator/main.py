from typing import List, Dict

import eventlet
import socketio

from loguru import logger

from queue_simulator.shared.experiments import SimulationSocketExperiment
from queue_simulator.socket_server.controllers import (
    BuilderController,
    SimulationController,
)
from queue_simulator.socket_server.socket_server import sio

app = socketio.WSGIApp(
    sio, static_files={"/": {"content_type": "text/html", "filename": "index.html"}}
)


@sio.event
def connect(sid, environ):
    logger.info("Client connected: {sid}", sid=sid)
    session: Dict[str, SimulationSocketExperiment]
    with sio.session(sid) as session:
        session["experiment"] = SimulationSocketExperiment(sio, sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


controllers = [BuilderController(), SimulationController()]

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("localhost", 4000)), app)
