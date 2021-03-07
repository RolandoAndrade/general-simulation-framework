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

        if self._inputs[model.getID()] is not None:
            self._inputs[model.getID()].append(input_model.getID())
        else:
            self._inputs[model.getID()] = [input_model.getID()]

    def getOutput(self) -> Dict[str, Any]:
        for model in self._models:
            self._outputs[model] = self._models[model].getOutput()
        return self._outputs

    def stateTransition(self, inputs: Dict[str, Any]):
        for model in inputs:
            if model in self._models:
                self._models[model].stateTransition(inputs[model])
