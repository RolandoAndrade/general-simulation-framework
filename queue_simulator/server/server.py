from typing import Any, List

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from queue_simulator.buffer.buffers.input_buffer import InputBuffer
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.buffers.process_buffer import ProcessBuffer
from queue_simulator.server.server_state import ServerState


class Server(DiscreteEventModel):
    """Server of processes"""

    processingTime: ExpressionProperty
    """Processing time of the server"""

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem,
                 name: str, ):
        super().__init__(dynamic_system,
                         name,
                         ServerState(
                             InputBuffer(name),
                             OutputBuffer(name),
                             ProcessBuffer(name)
                         )
                         )

    def _internalStateTransitionFunction(self, state: ServerState) -> ServerState:
        state.outputBuffer.add(state.processBuffer.empty())
        for i in range(state.inputBuffer.currentNumberOfEntities):
            if not state.processBuffer.isFull:
                state.processBuffer.add([state.inputBuffer.pop()])
            else:
                break
        if not state.inputBuffer.isEmpty:
            self.schedule(self.getTime())
        return state

    def _externalStateTransitionFunction(self, state: ServerState, inputs: List[Entity],
                                         event_time: float) -> ServerState:
        rest = 0
        if (state.inputBuffer.currentNumberOfEntities == 0 and
                len(inputs) > 0):
            self.schedule(self.getTime())
            rest = state.processBuffer.add(inputs)
        state.inputBuffer.add(inputs[rest:])
        return state

    def _timeAdvanceFunction(self, state: ServerState) -> float:
        if self.processingTime is not None:
            if state.inputBuffer.currentNumberOfEntities > 0:
                return self.processingTime.getValue().evaluate()
        return 0

    def _outputFunction(self, state: ServerState) -> Any:
        return state.outputBuffer.empty()

    def getProperties(self) -> EntityProperties:
        return {

        }
