from __future__ import annotations

from abc import abstractmethod
from typing import Any, Set, TYPE_CHECKING

from core.components.entity import Entity
from core.debug.domain.debug import debug

if TYPE_CHECKING:
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem

ModelState = Any


class BaseModel(Entity):
    """Base model in a dynamic system"""

    _serial_id = 0
    """Serial of the model"""

    __currentDynamicSystem: BaseDynamicSystem
    """Current dynamic system of the model"""

    __currentState: ModelState
    """Current state of the model"""

    __outputModels: Set[BaseModel]
    """Output models of the model"""

    @debug("Initialized Model", True)
    def __init__(
        self,
        dynamic_system: BaseDynamicSystem,
        name: str = None,
        state: ModelState = None,
    ):
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
        self.__currentDynamicSystem = dynamic_system
        self.__currentDynamicSystem.add(self)

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
            model (BaseModel): Output model to be added.
        """
        self.__currentDynamicSystem.add(model)
        self.__outputModels.add(model)

    @debug("Adding output")
    def remove(self, model: BaseModel):
        """Removes an specified output

        Args:
            model (BaseModel): Model to be removed.
        """
        if model in self.__outputModels:
            self.__outputModels.remove(model)

    @debug("Getting output models")
    def getOutputModels(self) -> Set[BaseModel]:
        """Returns the output models of the current model"""
        return self.__outputModels

    @debug("Retrieving dynamic system")
    def getDynamicSystem(self) -> BaseDynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self.__currentDynamicSystem

    @abstractmethod
    def getOutput(self) -> Any:
        """Gets the output of the model."""
        raise NotImplementedError

    @abstractmethod
    def stateTransition(self, *args, **kwargs):
        """Executes the state transition function"""
        raise NotImplementedError

    def __str__(self):
        name = self.getID()
        state = self.getState()
        return name + ": {'state': " + str(state) + "}"
