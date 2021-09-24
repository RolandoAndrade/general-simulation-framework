from abc import abstractmethod

from core.entity.core import EntityManager
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class DiscreteTimeModel(DiscreteEventModel):
    def __init__(
            self,
            dynamic_system: DiscreteEventDynamicSystem,
            name: str = None,
            state: ModelState = None,
            entity_manager: EntityManager = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
            entity_manager (EntityManager): Delegated entity manager.
        """
        super().__init__(dynamic_system, name, state, entity_manager)
        self.schedule(self.get_time())

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
