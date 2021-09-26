"""Base Model
==============
This module contains the definition of simulation Models.
It has an abstract definition BaseModel, that should be extended,
implementing its abstract methods.

Example:
    Creating a model::

        from models.core import BaseModel

        class Model(BaseModel):
            def get_output(self) -> int:
                return self.get_state()

            def state_transition(self, x: int, y: int):
                self.set_up_state(x + y)
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING

from gsf.core.debug.domain.debug import debug

from gsf.core.entity.core.entity import Entity
from gsf.core.entity.properties.expression_property import ExpressionProperty
from gsf.core.mathematics.values.value import Value
from gsf.models.core.path import Path

if TYPE_CHECKING:
    from gsf.core.entity.core import EntityManager
    from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem

ModelState = Any


class BaseModel(Entity):
    """Base model in a dynamic system

    Args:
        dynamic_system (BaseDynamicSystem): Dynamic system of the
            model.
        name (str): Name of the model.
        state (ModelState): Initial state of the model.
        entity_manager (EntityManager): Delegated entity manager.

    Attributes:
        BaseModel._serial_id (int): Serial of the model.
        __current_dynamic_system (BaseDynamicSystem): Current dynamic system of the model.
        __current_state (ModelState): Current state of the model.
    """

    _serial_id = 0

    __current_dynamic_system: BaseDynamicSystem

    __current_state: ModelState

    @debug("Initialized Model", True)
    def __init__(
        self,
        dynamic_system: BaseDynamicSystem,
        name: str = None,
        state: ModelState = None,
        entity_manager: EntityManager = None,
    ):
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
        """Sets up the state of the model.

        Args:
            state (ModelState): New state of the model.
        """
        self.__current_state = state

    @debug("Getting the state")
    def get_state(self) -> ModelState:
        """Returns the curren state,"""
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
