from typing import Dict, Any

from loguru import logger

from queue_simulator.queue_components.experiments import SimulationExperiment
from queue_simulator.socket_server.socket_server import sio


class ReportsController:
    @staticmethod
    @sio.event
    def get_report(sid, data: Dict[str, Any]):
        logger.info("Get report, sid: {sid}", sid=sid)
        session: Dict[str, SimulationExperiment]
        with sio.session(sid) as session:
            stats = session["experiment"].get_stats()
        return {"data": [s.serialize() for s in stats]}
