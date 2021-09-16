from typing import Dict

import socketio
from flask import Flask

from loguru import logger

from queue_simulator.queue_components.experiments import SimulationSocketExperiment
from queue_simulator.socket_server.controllers import (
    BuilderController,
    SimulationController,
    ReportsController,
)
from queue_simulator.socket_server.socket_server import sio

app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event
def connect(sid, environ):
    logger.info("Client connected: {sid}", sid=sid)
    session: Dict[str, SimulationSocketExperiment]
    with sio.session(sid) as session:
        session["experiment"] = SimulationSocketExperiment(sio, sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


controllers = [BuilderController(), SimulationController(), ReportsController()]

if __name__ == "__main__":
    app.run(port=4000)
