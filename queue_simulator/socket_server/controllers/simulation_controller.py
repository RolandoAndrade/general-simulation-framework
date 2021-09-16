from typing import Dict, Any

from loguru import logger

from queue_simulator.queue_components.experiments import SimulationExperiment
from queue_simulator.socket_server.socket_server import sio


class SimulationController:
    @staticmethod
    @sio.event
    def start_simulation(sid, data: Dict[str, Any]):
        stop_time = data.get("stopTime", None)
        step = data.get("stopTime", None)
        wait_time = data.get("waitTime", None)
        logger.info("Start simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            session["experiment"].start_simulation(stop_time, step, wait_time)
        return True

    @staticmethod
    @sio.event
    def stop_simulation(sid):
        logger.info("Stop simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            session["experiment"].simulation_control.stop()
        return True

    @staticmethod
    @sio.event
    def pause_simulation(sid):
        logger.info("Pause simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            session["experiment"].simulation_control.pause()
        return True
