from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, List, Union

if TYPE_CHECKING:
    from dynamic_system.models.discrete_time_model import DiscreteTimeModel


class DynamicSystem:
    _models: Dict[str, DiscreteTimeModel]
    _inputs: Dict[str, List[str]]
    _outputs: Dict[str, Any]

    def __init__(self):
        self._models = dict()
        self._inputs = dict()
        self._outputs = dict()

    def add(self, model: DiscreteTimeModel):
        """Add a model to the dynamic system.
        :param model: Model to be added."""
        self._models[model.getID()] = model

    def addInput(self, model: DiscreteTimeModel, input_model: DiscreteTimeModel):
        """Add a model as an input for the model.
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
        """Get the output of all the models in the dynamic system"""
        for model in self._models:
            self._outputs[model] = self._models[model].getOutput()
        return self._outputs

    def _getValuesToInject(self, input_models: List[str]) -> Union[Dict[str, Any], Any]:
        """Get the output of the input models that will be injected.
        :param input_models: Input models of the model.
        """
        if len(input_models) > 1:
            values = dict()
            for inp in input_models:
                values[inp] = self._outputs[inp]
            return values
        else:
            return self._outputs[input_models[0]]

    def stateTransition(self, input_models_values: Dict[str, Any] = {}):
        """Execute the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        :param input_models_values: Dictionary with key the identifier of the model
        and value the inputs for that model.
        """
        for model in input_models_values:
            self._models[model].stateTransition(input_models_values[model])
        for model in self._inputs:
            if model not in input_models_values:
                vs = self._getValuesToInject(self._inputs[model])
                self._models[model].stateTransition(vs)
