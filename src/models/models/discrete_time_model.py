from abc import abstractmethod

from core.types import Time
from core.types.model_input import ModelInput
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class DiscreteTimeModel(DiscreteEventModel):
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(self, state: ModelState, inputs: ModelInput,
                                            event_time: Time) -> ModelState:
        return self._state_transition(state, inputs, event_time)

    def _time_advance_function(self, state: ModelState) -> Time:
        return Time(1)

    @abstractmethod
    def _state_transition(self, state: ModelState, inputs: ModelInput,
                          event_time: Time) -> ModelState:
        raise NotImplementedError
