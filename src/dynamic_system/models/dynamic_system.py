from __future__ import annotations

from typing import Set, TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from dynamic_system.models.discrete_time_model import DiscreteTimeModel


class DynamicSystem:
    _models: Set[DiscreteTimeModel]
    _inputs: Dict[str, List[str]]
    _outputs: Dict[str, Any]

    def __init__(self):
        self._models = set()

    def add(self, model: DiscreteTimeModel):
        self._models.add(model)

    def addInput(self, model: DiscreteTimeModel, input_model: DiscreteTimeModel):
        self._models.add(input_model)
        if self._inputs[model.getID()] is not None:
            self._inputs[model.getID()].append(input_model.getID())
        else:
            self._inputs[model.getID()] = [input_model.getID()]
        
    def computeOutput(self):
        for model in self._models:
            self._outputs[model.getID()] = model.getOutput()

    def getOutput(self) -> Dict[str, Any]:
        return self._outputs
