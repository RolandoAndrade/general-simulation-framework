from typing import Dict, Any

from loguru import logger
from socketio import Server

from control.core import SimulationStats
from core.events import DomainEvents
from queue_simulator.queue_components.experiments.simulation_experiment import (
    SimulationExperiment,
)


class SimulationSocketExperiment(SimulationExperiment):
    _sio: Server
    _sid: str

    _last_labels_values: Dict[str, Any]

    def __init__(self, sio: Server, sid: str):
        super().__init__()
        self._sio = sio
        self._sid = sid
        self.event_bus.on(DomainEvents.SIMULATION_STATUS)(self.on_simulation_status)
        self.event_bus.on(DomainEvents.SIMULATION_FINISHED)(self.on_simulation_finished)
        self.event_bus.on("state_changed")(self.on_state_changed)
        self._last_labels_values = {}

    def on_simulation_status(self, data: SimulationStats):
        logger.info("Simulation status changed {data}, {sid}", data=data, sid=self._sid)
        self._sio.emit(
            DomainEvents.SIMULATION_STATUS,
            {
                "time": float(data.time),
                "stopTime": float(data.stop_time),
                "frequency": float(data.frequency),
                "isPaused": data.is_paused,
            },
            self._sid,
        )
        self.__emit_labels()

    def on_simulation_finished(self):
        logger.info("Simulation finished, {sid}", sid=self._sid)
        self._sio.emit(DomainEvents.SIMULATION_FINISHED, to=self._sid)
        self.__emit_labels()

    def on_simulation_paused(self):
        logger.info("Simulation paused, {sid}", sid=self._sid)
        self._sio.emit(DomainEvents.SIMULATION_PAUSED, to=self._sid)

    def on_simulation_stopped(self):
        logger.info("Simulation stopped, {sid}", sid=self._sid)
        self._sio.emit(DomainEvents.SIMULATION_STOPPED, to=self._sid)

    def on_state_changed(self, data):
        self._sio.emit("STATE_CHANGED", {
            'name': data['name'],
            'state': {
                'inputBuffer': data['state'].get('input_buffer', None),
                'outputBuffer': data['state'].get('output_buffer', None),
                'processBuffer': data['state'].get('process_buffer', None)
            }
        }, self._sid)

    def __emit_labels(self):
        new_labels = self.get_labels_values()
        if self._last_labels_values != new_labels:
            self._last_labels_values = new_labels
            self._sio.emit("LABELS_CHANGED", new_labels, self._sid)


    def save(self):
        self.simulation_control.stop()
        ax_sid = self._sid
        ax_sio = self._sio
        self._sid = None
        self._sio = None
        data = super().save()
        self._sid = ax_sid
        self._sio = ax_sio
        return data

    def load(self, data: str):
        recovered = super().load(data)
        recovered._sid = self._sid
        recovered._sio = self._sio
        return recovered

    def get_labels_values(self):
        labels_values: Dict[str, Any] = {}
        for label in self._labels:
            labels_values.update({label.get_id(): label.get_value()})
        return labels_values
