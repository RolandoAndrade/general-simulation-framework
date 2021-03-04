from __future__ import annotations
from abc import abstractmethod
from typing import Any

from dynamic_system.models.base_model import BaseModel

from dynamic_system.utils.bag_of_values import BagOfValues


class DiscreteTimeModel(BaseModel):
    _currentState: Any

    def __init__(self, name: str = None):
        super().__init__(name)
        self._currentState = None

    def receiveInput(self, model_id: str, inputs: BagOfValues):
        pass

    def setUpState(self, state: Any):
        """s

        Sets up the state of the model.

        :param state: New state of the model.
        """
        self._currentState = state

    def stateTransition(self, inputs: Any):
        """Executes the state transition using the state given by
        the state transition function.

        :param inputs: Input trajectory x.
        """
        new_state = self.stateTransitionFunction(self._currentState, inputs)
        self.setUpState(new_state)

    def getOutput(self) -> Any:
        """Get the output of the model.

        :returns y: output trajectory y.
        """
        return self.outputFunction(self._currentState)

    @abstractmethod
    def stateTransitionFunction(self, state: BagOfValues, inputs: Any) -> Any:
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

    @abstractmethod
    def outputFunction(self, state: Any) -> Any:
        """.. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer.

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        :param state: current state s of the model.

        :returns y: output trajectory y.
        """
        pass
