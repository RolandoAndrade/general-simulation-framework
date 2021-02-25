from typing import Dict, Union

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


class InputManager:
    _inputs: Dict[int, Union[BagOfValues, None]]

    def save_input(self, model_id: int, inputs: Union[BagOfValues, None]):
        self._inputs[model_id] = inputs

    def is_ready(self) -> bool:
        for inp in self._inputs:
            if self._inputs[inp] is None:
                return False
        return True

    def add_input(self, model_id: int):
        self.save_input(model_id, None)

    def remove_input(self, model_id):
        self._inputs.pop(model_id)

    def clear(self):
        for inp in self._inputs:
            self._inputs[inp] = None
