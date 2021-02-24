from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues
    from dynamic_system.base_model import BaseModel


class InputBag:
    _model: BaseModel
    _output: BagOfValues

    def __init__(self, model: BaseModel, output: BagOfValues):
        self._model = model
        self._output = output

    def get_model(self) -> BaseModel:
        return self._model

    def equals_model(self, input_bag: InputBag) -> bool:
        return self.get_model() == input_bag.get_model()