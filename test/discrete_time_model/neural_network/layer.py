from __future__ import annotations

from random import random
from typing import Dict, List

from dynamic_system.models.discrete_time_model import DiscreteTimeModel
from dynamic_system.models.dynamic_system import DynamicSystem


class Layer(DiscreteTimeModel):
    _weights: List[List[float]]

    def __init__(self, dynamic_system: DynamicSystem, n_neurons: int, inputs: int):
        super().__init__(dynamic_system)
        self._weights = []
        for i in range(n_neurons):
            neuron = []
            for j in range(inputs):
                neuron.append(random())
            self._weights.append(neuron)
        self.setUpState([[0]]*n_neurons)

    def stateTransitionFunction(self, state: bool, inputs: List[List[float]]) -> List[List[float]]:
        outs = []
        for neuron in range(len(self._weights)):
            neuron_out = 0
            for weight in range(len(self._weights[neuron])):
                neuron_out += self._weights[neuron][weight] * inputs[weight][0]
            outs.append([neuron_out])
        return outs

    def outputFunction(self, state: bool) -> bool:
        return state