from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.model import Model
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


class SimulationEngine:
    _model: Model
    _is_output_up_to_date: bool
    _time_of_last_event: float
    _time_of_next_event: float

    def __init__(self, atomic_model: Model):
        self._model = atomic_model

    def get_time(self) -> int:
        """Returns the simulation time at which the state was last computed"""
        return self._time

    def next_event_time(self) -> float:
        """Returns the time of the next autonomous action

        :returns time of the next autonomous action"""
        return self._time_of_next_event

    def compute_next_state(self, inputs: BagOfValues, time: float):
        """Computes the next state with external, internal or confluent state transition function

        :param time:
        :param inputs: Inputs for next state
        """
        if time < self._time_of_next_event and not inputs.is_empty():  # If this is an external event
            self._model.external_state_transition_function(inputs, time - self._time_of_last_event)
        elif time == self._time_of_next_event:
            # Confluent with autonomous action
            self.compute_output()  # Compute the output at the time
            if not inputs.is_empty():
                # If input is not empty is external event
                self._model.confluent_state_transition_function(inputs)
            else:
                # Internal event
                self._model.internal_state_transition_function()

        self._time_of_next_event = self._time_of_next_event + self._model.time_advance_function()
        self._time_of_last_event = time

        # event_bus.emit("STATE_CHANGED") # TODO Notify listeners that the state has changed
        self._is_output_up_to_date = False

    def execute_next_event(self):
        """Computes the output and next state of the model at the next event time"""
        self.compute_next_state(BagOfValues(), self.next_event_time())

    def compute_output(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if not self._is_output_up_to_date:
            self._is_output_up_to_date = True
            self._model.compute_output()
            # event_bus.emit("OUTPUT") # TODO Notify listeners that the there is an output
