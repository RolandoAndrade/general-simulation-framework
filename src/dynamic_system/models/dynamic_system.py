from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, List

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
        self._models[model.getID()] = model

    def addInput(self, model: DiscreteTimeModel, input_model: DiscreteTimeModel):
        if model.getDynamicSystem() != input_model.getDynamicSystem():
            raise Exception("Dynamic system of the models does not match")
        if model.getDynamicSystem() != self or input_model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")

        if model.getID() in self._inputs:
            self._inputs[model.getID()].append(input_model.getID())
        else:
            self._inputs[model.getID()] = [input_model.getID()]

    def getOutput(self) -> Dict[str, Any]:
        for model in self._models:
            self._outputs[model] = self._models[model].getOutput()
        return self._outputs

    def _getValuesToInject(self, models: List[str], input_models_values: Dict[str, Any]):
        if len(models) > 1:
            l = []
            for inp in models:
                l.append({inp: input_models_values[inp]})
            return l
        else:
            return input_models_values[models[0]]

    def stateTransition(self, input_models_values: Dict[str, Any]):
        for model in self._inputs:
            input_of_model = self._getValuesToInject(self._inputs[model], input_models_values)
            self._models[model].stateTransition(input_of_model)
