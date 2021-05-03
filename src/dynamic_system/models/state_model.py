from __future__ import annotations

from abc import abstractmethod
from typing import Any

from dynamic_system.models.base_model import BaseModel
from dynamic_system.models.dynamic_system import DynamicSystem


class StateModel(BaseModel):
    """Model with an state"""
    _currentState: Any
    _currentDynamicSystem: DynamicSystem

    def __init__(self, dynamic_system: DynamicSystem, name: str = None, state=None):
        """
        Args:
            dynamic_system (DynamicSystem): Dynamic system of the model.
            name (str): Name of the model.
            state (Any): Initial state of the model.
        """
        super().__init__(name)
        # Init the model
        self.setUpState(state)
        # Add the model to the dynamic system
        self._currentDynamicSystem = dynamic_system
        self._currentDynamicSystem.add(self)

    def add(self, model: StateModel):
        """Adds a model as an input for the current model in the dynamic system.

        Args:
            model (StateModel):Model to be an input.
        """
        self._currentDynamicSystem.addInput(self, model)

    def getDynamicSystem(self) -> DynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self._currentDynamicSystem

    def getOutput(self) -> Any:
        """Gets the output of the model."""
        return self.outputFunction(self._currentState)

    def setUpState(self, state: Any):
        """s

        Sets up the state of the model.

        Args:
            state (Any): New state of the model.
        """
        self._currentState = state

    @abstractmethod
    def outputFunction(self, state: Any) -> Any:
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer.

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (Any): Current state s of the model.
        """
        pass

    @abstractmethod
    def stateTransition(self, *args, **kwargs):
        """Executes the state transition.

        Args:
            *args:
            **kwargs:
        """
        pass

    def getTime(self) -> float:
        """Gets the time of the next autonomous event."""
        return 1
