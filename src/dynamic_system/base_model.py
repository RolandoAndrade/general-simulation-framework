from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues

from abc import abstractmethod



class BaseModel:
    _id: int
    _serial_id = 0

    def __init__(self):
        _id = BaseModel._serial_id
        BaseModel._serial_id = BaseModel._serial_id + 1

    _listeners: List[BaseModel]

    def _add_listener(self, model: BaseModel):
        self._listeners.append(model)

    def _remove_listener(self, model: BaseModel):
        self._listeners.remove(model)

    def get_id(self):
        return self._id

    @abstractmethod
    def receive_input(self, model_id: int, inputs: BagOfValues):
        pass