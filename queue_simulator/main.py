from typing import List, Dict


import eventlet
import socketio
from flask import Flask

from loguru import logger

from core.events import DomainEvents
from queue_simulator.shared.experiments import SimulationSocketExperiment
from queue_simulator.socket_server.controllers import (
    BuilderController,
    SimulationController,
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


controllers = [BuilderController(), SimulationController()]

if __name__ == "__main__":
    """eventlet.monkey_patch(os=True,
                          select=True,
                          socket=True,
                          thread=False,
                          time=True)
    eventlet.wsgi.server(eventlet.listen(("localhost", 4000)), app)"""
    app.run(port=4000)
