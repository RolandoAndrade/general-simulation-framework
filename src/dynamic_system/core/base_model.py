from __future__ import annotations

from abc import abstractmethod
from typing import Any, Set, TYPE_CHECKING

from core.components.entity import Entity
from core.debug.domain.debug import debug

if TYPE_CHECKING:
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem

ModelState = Any


class BaseModel(Entity):
    """DiscreteEventModel in a dynamic system"""

    _serial_id = 0
    """Serial of the model"""

    _currentDynamicSystem: BaseDynamicSystem
    """Current dynamic system of the model"""

    __currentState: ModelState
    """Current state of the model"""

    __outputModels: Set[BaseModel]
    """Output models of the model"""

    @debug("Initialized Model", True)
    def __init__(self,
                 dynamic_system: BaseDynamicSystem,
                 name: str = None,
                 state: ModelState = None, ):
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
        """
        # Init the model
        if name is None:
            self.setID("model" + str(BaseModel._serial_id))
            BaseModel._serial_id = BaseModel._serial_id + 1
        else:
            self.setID(name)
        self.setUpState(state)
        self.__outputModels = set()
        # Set dynamic system
        self._currentDynamicSystem = dynamic_system
        self._currentDynamicSystem.add(self)

    @debug("Setting up the state")
    def setUpState(self, state: ModelState):
        """s

        Sets up the state of the model.

        Args:
            state (ModelState): New state of the model.
        """
        self.__currentState = state

    @debug("Getting the state")
    def getState(self) -> ModelState:
        """Returns the current state"""
        return self.__currentState

    @debug("Adding output")
    def add(self, model: BaseModel):
        """Adds a model as an input for the current model in the dynamic system.

        Args:
            model (DiscreteEventModel): Model to be an input.
        """
        self._currentDynamicSystem.add(model)
        self.__outputModels.add(model)

    @debug("Getting output models")
    def getOutputModels(self) -> Set[BaseModel]:
        """Returns the output models of the current model"""
        return self.__outputModels

    @debug("Retrieving dynamic system")
    def getDynamicSystem(self) -> BaseDynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self._currentDynamicSystem

    @debug("Getting output")
    def getOutput(self) -> Any:
        """Gets the output of the model."""
        return self._outputFunction(self.__currentState)

    @abstractmethod
    def _outputFunction(self, state: ModelState) -> Any:
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer when e=ta(s).

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (ModelState): current state s of the model.
        """
        raise NotImplementedError

    @abstractmethod
    def stateTransition(self, *args, **kwargs):
        """Executes the state transition function"""
        raise NotImplementedError

    @abstractmethod
    def summary(self):
        """Prints a summary of the model"""
        raise NotImplementedError

    def __str__(self):
        name = self.getID()
        state = self.getState()
        return name + ": {'state': " + str(state) + "}"