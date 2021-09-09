from typing import Dict

from loguru import logger

from queue_simulator.shared.experiments import SimulationExperiment
from queue_simulator.socket_server.socket_server import sio


class SimulationController:
    @staticmethod
    @sio.event
    def start_simulation(sid, data):
        stop_time = data["stopTime"]
        logger.info("Start simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            session["experiment"].start_simulation(
                stop_time=stop_time
            )
        return True

    @staticmethod
    @sio.event
    def stop_simulation(sid, data):
        logger.info("Start simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session["experiment"].simulation_control.stop()
        return created_path.serialize()

    @staticmethod
    @sio.event
    def pause_simulation(sid, data):
        logger.info("Start simulation, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            created_path = session["experiment"].simulation_control.pause()
        return created_path.serialize()
