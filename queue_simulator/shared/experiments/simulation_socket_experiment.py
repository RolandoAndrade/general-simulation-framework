import threading

from loguru import logger
from socketio import Server

from control.core import SimulationStats
from core.events import DomainEvents
from core.types import Time
from queue_simulator.shared.experiments.simulation_experiment import (
    SimulationExperiment,
)


class SimulationSocketExperiment(SimulationExperiment):
    _sio: Server
    _sid: str

    def __init__(self, sio: Server, sid: str):
        super().__init__()
        self._sio = sio
        self._sid = sid
        self.event_bus.on(DomainEvents.SIMULATION_STATUS)(self.on_simulation_status)
        self.event_bus.on(DomainEvents.SIMULATION_FINISHED)(self.on_simulation_finished)

    def on_simulation_status(self, data: SimulationStats):
        logger.info("Simulation status changed {data}, {sid}", data=data, sid=self._sid)
        self._sio.emit(DomainEvents.SIMULATION_STATUS, {
            'time': float(data.time),
            'stopTime': float(data.stop_time),
            'frequency': float(data.frequency),
            'isPaused': data.is_paused
        }, self._sid)

    def on_simulation_finished(self):
        self._sio.emit(DomainEvents.SIMULATION_FINISHED, to=self._sid)
