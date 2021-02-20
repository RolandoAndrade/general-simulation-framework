from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_model.atomic_model import AtomicModel
    from dynamic_system.atomic_model.bag_of_values import BagOfValues


class SimulationEngine:
    _atomic_model: AtomicModel
    _time: int  # TODO unsigned
    _is_output_up_to_date: bool

    def __init__(self, atomic_model: AtomicModel):
        self._atomic_model = atomic_model

    def get_time(self) -> int:
        """Returns the simulation time at which the state was last computed"""
        return self._time

    def compute_next_state(self, inputs: BagOfValues):
        """First computes model's output function if this has not already been done, then
        computes the model's next state and notifies listeners of these actions and finally
        tells the model to clean up objects created by its output function

        :param inputs: Inputs for next state
        """
        self.compute_output()  # Compute the output at time t
        self._time = self._time + 1  # Advance simulation clock
        self._atomic_model.state_transition_function(inputs)  # Compute the new state of the model
        # event_bus.emit("STATE_CHANGED") # TODO Notify listeners that the state has changed
        self._is_output_up_to_date = False

    def compute_output(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if self._is_output_up_to_date:  # Just evaluate once per time
            return
        self._is_output_up_to_date = True
        self._atomic_model.compute_output()
        # event_bus.emit("OUTPUT") # TODO Notify listeners that the there is an output
