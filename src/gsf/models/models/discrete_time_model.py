"""Discrete Time Model
==============
This module contains the definition of a discrete time simulation Model.
It has an abstract definition DiscreteTimeModel, that should be extended,
implementing its abstract methods.

Example:
    Creating a model::

        class Cell(DiscreteTimeModel):
            _symbol: str

            def __init__(
                self,
                dynamic_system: DiscreteEventDynamicSystem,
                state: bool,
                symbol: str = None,
            ):
                super().__init__(dynamic_system, state=state)
                self._symbol = symbol or "\u2665"

            def _state_transition(self, state: bool, inputs: Dict[BaseModel, bool]) -> bool:
                next_state: bool = list(inputs.values())[0]
                return next_state

            def _output_function(self, state: bool) -> bool:
                return state

            def __str__(self):
                is_alive = self.get_state()
                if is_alive:
                    return self._symbol
                return "-"
"""


from abc import abstractmethod

from gsf.core.entity.core import EntityManager
from gsf.core.types import Time
from gsf.core.types.model_input import ModelInput
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.core.base_model import ModelState
from gsf.models.models import DiscreteEventModel


class DiscreteTimeModel(DiscreteEventModel):
    """DiscreteTimeModel

    Discrete-time views values of variables as occurring at distinct, separate
    "points in time", or equivalently as being unchanged throughout each non-zero region of time,
    time is viewed as a discrete variable
    """

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

    def _external_state_transition_function(
        self, state: ModelState, inputs: ModelInput, event_time: Time
    ) -> ModelState:
        return self._state_transition(state, inputs)

    def _time_advance_function(self, state: ModelState) -> Time:
        return Time(1)

    @abstractmethod
    def _state_transition(self, state: ModelState, inputs: ModelInput) -> ModelState:
        """Executes the state transition using the current state of the model.

         .. math:: \delta \; : \; S \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
        """
        raise NotImplementedError
