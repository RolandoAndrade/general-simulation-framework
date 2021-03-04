from __future__ import annotations
from dynamic_system.models.input_model import InputModel
from dynamic_system.utils.bag_of_values import BagOfValues


class InputLayer(InputModel):
    def __init__(self, name: str):
        super().__init__(name)

    def set_inputs(self, values: BagOfValues):
        self._inputs = values