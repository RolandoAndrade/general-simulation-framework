from __future__ import annotations
from abc import abstractmethod

from dynamic_system.models.base_model import BaseModel

from dynamic_system.utils.bag_of_values import BagOfValues

class DiscreteTimeModel(BaseModel):
    _currentState: BagOfValues

    def __init__(self, name: str = None):
        super().__init__(name)
        self._currentState = BagOfValues()

    def receiveInput(self, model_id: str, inputs: BagOfValues):
        pass

    @abstractmethod
    def internalStateTransitionFunction(self, s: BagOfValues, x: BagOfValues) -> BagOfValues:
        """.. math:: \delta \; (s,x)

        Implements the internal state transition function delta.
        The internal state transition function moves the system
        from a state s to a state s' in response to the input trajectory x.

         .. math:: \delta \; : \; S \; x \; X \longrightarrow S

         :param s: Current state of the model.
         :param x: Input trajectory.

         :return s: New state s'
        """
        pass

    @abstractmethod
    def outputFunction(self, s: BagOfValues) -> BagOfValues:
        """.. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer.

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        :param s: current state of the model.

        :returns y: output trajectory y.
        """
        pass

    def setUpState(self, s: BagOfValues):
        pass