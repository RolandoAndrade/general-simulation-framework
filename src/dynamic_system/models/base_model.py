from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues

from abc import abstractmethod


class BaseModel:
    """"Model in a dynamic system
    """
    _id: int
    _serial_id = 0
    _listeners: List[BaseModel]

    def __init__(self):
        self._id = BaseModel._serial_id
        BaseModel._serial_id = BaseModel._serial_id + 1
        self._listeners = []

    def add_listener(self, model: BaseModel):
        """Add a model to listeners
        :param model Model that will be listen
        """
        self._listeners.append(model)

    def remove_listener(self, model: BaseModel):
        """Remove a model from listeners
        :param model Model to be removed
        """
        self._listeners.remove(model)

    def get_id(self) -> int:
        """Returns the identifier of the model"""
        return self._id

    def notify_output(self, out: BagOfValues):
        """Notifies to listeners the arrival of an output
        :param out Output that will be an input for a listener"""
        for model in self._listeners:
            model.receive_input(self.get_id(), out)

    @abstractmethod
    def receive_input(self, model_id: int, inputs: BagOfValues):
        """Receive the output from a model that is an input for the current model
        :param model_id ID of the model that emits the input
        :param inputs Output of the model that serves of input for the current model
        """
        pass

    def summary(self):
        """Print a summary of the model"""
        row_format = "{:>15}" * 5
        print(row_format.format("", *["ID", "TYPE", "NAME", "INPUTS", "OUTPUTS"]))
