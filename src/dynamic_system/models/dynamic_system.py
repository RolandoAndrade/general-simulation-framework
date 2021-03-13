from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, List, Union

from dynamic_system.control.scheduler import Scheduler

if TYPE_CHECKING:
    from dynamic_system.models.state_model import StateModel


class DynamicSystem:
    _models: Dict[str, StateModel]  # All the models in the dynamic system
    _inputs: Dict[str, List[str]]   # Models and their models that act as an input
    _outputs: Dict[str, Any]        # Output of all the models

    def __init__(self):
        self._models = dict()
        self._inputs = dict()
        self._outputs = dict()

    def add(self, model: StateModel):
        """Adds a model to the dynamic system.
        :param model: Model to be added."""
        self._models[model.getID()] = model

    def addInput(self, model: StateModel, input_model: StateModel):
        """Adds a model as an input for the given model.
        :param model: Destination model.
        :param input_model: Model defined as an input."""
        if model.getDynamicSystem() != input_model.getDynamicSystem():
            raise Exception("Dynamic system of the models does not match")
        if model.getDynamicSystem() != self or input_model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")

        if model.getID() in self._inputs:
            self._inputs[model.getID()].append(input_model.getID())
        else:
            self._inputs[model.getID()] = [input_model.getID()]

    def getOutput(self) -> Dict[str, Any]:
        """Gets the output of all the models in the dynamic system"""
        for model in self._models:
            self._outputs[model] = self._models[model].getOutput()
        return self._outputs

    def _getValuesToInject(self, input_models: List[str]) -> Union[Dict[str, Any], Any]:
        """Gets the output of the input models that will be injected.
        :param input_models: Input models of the model.
        """
        if len(input_models) > 1:
            values = dict()
            for inp in input_models:
                values[inp] = self._outputs[inp]
            return values
        else:
            return self._outputs[input_models[0]]

    def stateTransition(self, input_models_values: Dict[str, Any] = None):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        :param input_models_values: Dictionary with key the identifier of the model
        and value the inputs for that model.
        """
        if input_models_values is None:
            input_models_values = {}

        for model in input_models_values:
            self._models[model].stateTransition(input_models_values[model])
        for model in self._inputs:
            if model not in input_models_values:
                vs = self._getValuesToInject(self._inputs[model])
                self._models[model].stateTransition(vs)
