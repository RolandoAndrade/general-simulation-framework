from socketio import Server

from core.events import EventBus, DomainEvents
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

    def on_simulation_status(self, data):
        self._sio.emit(DomainEvents.SIMULATION_STATUS, data, self._sid)
