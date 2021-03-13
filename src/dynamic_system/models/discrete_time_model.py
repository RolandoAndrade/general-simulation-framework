from __future__ import annotations
from abc import abstractmethod
from typing import Any, Set

from dynamic_system.models.state_model import StateModel

from dynamic_system.utils.bag_of_values import BagOfValues


class DiscreteTimeModel(StateModel):
    def stateTransition(self, inputs: Any):
        """Executes the state transition using the state given by
        the state transition function.

        :param inputs: Input trajectory x.
        """
        new_state = self.stateTransitionFunction(self._currentState, inputs)
        self.setUpState(new_state)

    @abstractmethod
    def stateTransitionFunction(self, state: Any, inputs: Any) -> Any:
        """.. math:: \delta \; (s,x)

        Implements the internal state transition function delta.
        The internal state transition function moves the system
        from a state s to a state s' in response to the input trajectory x.

         .. math:: \delta \; : \; S \; x \; X \longrightarrow S

         :param state: Current state s of the model.
         :param inputs: Input trajectory x.

         :return s: New state s'
        """
        pass


