from typing import Any, List

from core.components.entity.entity import Entity
from models.core.base_model import ModelState
from models.models.discrete_event_model import ModelInput
from test.queue_simulator.buffer.buffer import Buffer


class OutputBuffer(Buffer):
    def _internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        return state

    def _externalStateTransitionFunction(self, state: ModelState, inputs: ModelInput, event_time: float) -> ModelState:
        state['numberEntered'] += inputs['entitiesPerArrival']
        state['contents'] = []
        for i in range(inputs['entitiesPerArrival']):
            state['contents'].append(inputs['entity'])
        return state

    def _timeAdvanceFunction(self, state: ModelState) -> float:
        return self._time

    def _outputFunction(self, state: ModelState) -> List[Entity]:
        return state['contents']
