from typing import Dict, Union

from typing import TYPE_CHECKING

from dynamic_system.utils.value import Value

if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues


class InputManager:
    """Manage the inputs received in a model"""
    _inputs: Dict[int, Union[BagOfValues, None]]

    def save_input(self, model_id: int, inputs: Union[BagOfValues, None]):
        """Save an input for a model output
        :param model_id: Model that throw the output
        :param inputs: Inputs given by the output model
        """
        self._inputs[model_id] = inputs

    def is_ready(self) -> bool:
        """Check if there are no missing inputs"""
        for inp in self._inputs:
            if self._inputs[inp] is None:
                return False
        return True

    def add_input(self, model_id: int):
        """Define the initial input models"""
        self.save_input(model_id, None)

    def remove_input(self, model_id):
        """Remove a model from required inputs"""
        self._inputs.pop(model_id)

    def clear(self):
        """Clear all the received inputs"""
        for inp in self._inputs:
            self._inputs[inp] = None

    def get_inputs(self) -> BagOfValues:
        """Get the inputs thrown by the outputs of the defined models. Return a
        BagOfValues with the template m-<id>: BagOfValues returned by all the models
        """
        values = list(self._inputs.values())
        names = self._inputs.keys()
        vs = []
        for name in names:
            vs.append(Value("m-" + str(name), values))
        return BagOfValues(vs)
