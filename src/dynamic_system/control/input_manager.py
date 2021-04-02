from __future__ import annotations

from typing import Union

from dynamic_system.utils.bag_of_values import BagOfValues


class InputManager:
    """Manage the inputs received in a model"""
    _inputs: BagOfValues

    def __init__(self):
        self._inputs = BagOfValues()

    def saveInput(self, model_id: str, inputs: Union[BagOfValues, None]):
        """Save an input for a model output
        :param model_id: Model that throw the output
        :param inputs: Inputs given by the output model
        """
        self._inputs[model_id] = inputs

    def isReady(self) -> bool:
        """Check if there are no missing inputs"""
        for inp in self._inputs:
            if self._inputs[inp] is None:
                return False
        return True

    def addInput(self, model_id: str):
        """Define the initial input models"""
        self.saveInput(model_id, None)

    def removeInput(self, model_id):
        """Remove a model from required inputs"""
        self._inputs.pop(model_id)

    def clear(self):
        """Clear all the received inputs"""
        for inp in self._inputs:
            self._inputs[inp] = None

    def getInputs(self) -> BagOfValues:
        """Get the inputs thrown by the outputs of the defined models. Return a
        BagOfValues with the template <id>: BagOfValues returned by all the models
        """
        return self._inputs.copy()
