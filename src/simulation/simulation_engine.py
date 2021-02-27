from __future__ import annotations

from typing import TYPE_CHECKING

from core.events.event_bus import event_bus
from dynamic_system.events.compute_output_event import ComputeOutputEvent

if TYPE_CHECKING:
    from dynamic_system.model import Model


class SimulationEngine:
    _model: Model
    _is_output_up_to_date: bool
    _time_of_last_event: float
    _time_of_next_event: float

    def __init__(self, atomic_model: Model):
        self._model = atomic_model

    def next_event_time(self) -> float:
        """Returns the time of the next autonomous action

        :returns time of the next autonomous action"""
        return self._time_of_next_event

    def compute_next_state(self, time: float, is_external=True):
        """Computes the next state with external, internal or confluent state transition function

        :param time: Time of the event
        :param is_external: Is an external event
        """
        if time < self._time_of_next_event and is_external:  # If this is an external event
            self._model.external_state_transition_function(time - self._time_of_last_event)
        elif time == self._time_of_next_event:  # Confluent with autonomous action
            self.compute_output()  # Compute the output at the time
            if is_external:
                self._model.confluent_state_transition_function()
            else:
                self._model.internal_state_transition_function()

        self._time_of_next_event = self._time_of_next_event + self._model.time_advance_function()
        self._time_of_last_event = time

        self._is_output_up_to_date = False

    def execute_next_event(self):
        """Computes the output and next state of the model at the next event time"""
        self.compute_next_state(self.next_event_time(), False)

    def compute_output(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if not self._is_output_up_to_date:
            self._is_output_up_to_date = True
            self._model.compute_output()
            event_bus.emit(ComputeOutputEvent)
