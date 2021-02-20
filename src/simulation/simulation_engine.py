from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_models.atomic_model import AtomicModel
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


class SimulationEngine:
    _model: AtomicModel
    _time: int  # TODO unsigned
    _is_output_up_to_date: bool

    def __init__(self, atomic_model: AtomicModel):
        self._model = atomic_model

    def get_time(self) -> int:
        """Returns the simulation time at which the state was last computed"""
        return self._time

    def compute_next_state(self, inputs: BagOfValues):
        """First computes model's output function if this has not already been done, then
        computes the model's next state and notifies listeners of these actions

        :param inputs: Inputs for next state
        """
        self.compute_output()  # Compute the output at time t
        self._time = self._time + 1  # Advance simulation clock
        self._model.state_transition_function(inputs)  # Compute the new state of the model
        # event_bus.emit("STATE_CHANGED") # TODO Notify listeners that the state has changed
        self._is_output_up_to_date = False

    def compute_output(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if not self._is_output_up_to_date:
            self._is_output_up_to_date = True
            self._model.compute_output()
            # event_bus.emit("OUTPUT") # TODO Notify listeners that the there is an output
