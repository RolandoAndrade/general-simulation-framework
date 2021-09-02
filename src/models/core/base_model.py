from __future__ import annotations

from abc import abstractmethod
from typing import Any, Set, TYPE_CHECKING, cast

from core.debug.domain.debug import debug

from core.entity.core.entity import Entity
from core.entity.properties.expression_property import ExpressionProperty
from core.mathematics.values.value import Value
from models.core.path import Path

if TYPE_CHECKING:
    from core.entity.core import EntityManager
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem

ModelState = Any


class BaseModel(Entity):
    """Base model in a dynamic system"""

    _serial_id = 0
    """Serial of the model"""

    __current_dynamic_system: BaseDynamicSystem
    """Current dynamic system of the model"""

    __current_state: ModelState
    """Current state of the model"""

    @debug("Initialized Model", True)
    def __init__(
        self,
        dynamic_system: BaseDynamicSystem,
        name: str = None,
        state: ModelState = None,
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
            entity_manager (EntityManager): Delegated entity manager.
        """
        # Init the model
        if name is None:
            super().__init__("model" + str(BaseModel._serial_id), entity_manager)
            BaseModel._serial_id = BaseModel._serial_id + 1
        else:
            super().__init__(name, entity_manager)
        self.set_up_state(state)
        # Set dynamic system
        self.__current_dynamic_system = dynamic_system
        self.__current_dynamic_system.add(self)

    @debug("Setting up the state")
    def set_up_state(self, state: ModelState):
        """s

        Sets up the state of the model.

        Args:
            state (ModelState): New state of the model.
        """
        self.__current_state = state

    @debug("Getting the state")
    def get_state(self) -> ModelState:
        """Returns the current state"""
        return self.__current_state

    @debug("Adding output")
    def add(
        self,
        model: BaseModel,
        weight: ExpressionProperty = ExpressionProperty(Value(1)),
        name: str = None,
    ):
        """Current model will be the input for the given model.

        Args:
            model (BaseModel): Output model to be added.
            weight (ExpressionProperty): Weight of the path.
            name (str): Name of the path.
        """
        return self.__current_dynamic_system.link(Path(self, model, weight, name))

    @debug("Removing")
    def remove(self):
        """Removes the model from the dynamic system"""
        self.__current_dynamic_system.remove(self)
        self._entity_manager.remove(self.get_id())

    @debug("Retrieving dynamic system")
    def get_dynamic_system(self) -> BaseDynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self.__current_dynamic_system

    @abstractmethod
    def get_output(self) -> Any:
        """Gets the output of the model."""
        raise NotImplementedError

    @abstractmethod
    def state_transition(self, *args, **kwargs):
        """Executes the state transition function"""
        raise NotImplementedError

    def __str__(self):
        name = self.get_id()
        state = self.get_state()
        return name + ": {'state': " + str(state) + "}"
