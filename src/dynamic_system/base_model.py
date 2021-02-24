from __future__ import annotations

from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues
    from dynamic_system.input_bag import InputBag

from abc import abstractmethod


class BaseModel:
    _listeners: List[BaseModel]

    def _add_listener(self, model: BaseModel):
        self._listeners.append(model)

    def _remove_listener(self, model: BaseModel):
        self._listeners.remove(model)

    @abstractmethod
    def receive_input(self, input_bag: InputBag):
        pass