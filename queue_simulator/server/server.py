from typing import Any, List, Union, Dict

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.expression_property import ExpressionProperty
from core.components.expresions.expression import Expression
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from queue_simulator.buffer.buffers.input_buffer import InputBuffer
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.buffers.process_buffer import ProcessBuffer
from queue_simulator.server.server_state import ServerState


class Server(DiscreteEventModel):
    """Server of processes"""

    _processingTime: ExpressionProperty
    """Processing time of the server"""

    _isBusy: bool
    """Processing time of the server"""

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem,
                 name: str,
                 processing_time: Union[ExpressionProperty, Expression] = None):
        super().__init__(dynamic_system,
                         name,
                         ServerState(
                             InputBuffer(name),
                             OutputBuffer(name),
                             ProcessBuffer(name)
                         )
                         )
        self.processingTime = processing_time
        self._isBusy = False

    def _process(self, state: ServerState):
        for i in range(state.inputBuffer.currentNumberOfEntities):
            if not state.processBuffer.isFull:
                state.processBuffer.add([state.inputBuffer.pop()])
                self._isBusy = True
            else:
                break

    def _internalStateTransitionFunction(self, state: ServerState) -> ServerState:
        self._isBusy = False
        state.outputBuffer.add(state.processBuffer.empty())
        self._process(state)
        # recalculate the processing time
        state.processingRemainingTime = self.processingTime.getValue().evaluate()
        if self._isBusy:
            self.schedule(self.getTime())
        return state

    def _externalStateTransitionFunction(self, state: ServerState,
                                         inputs: Dict[str, List[Entity]],
                                         event_time: float) -> ServerState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.inputBuffer.add(r_inputs)
        if not self._isBusy and len(r_inputs) > 0:
            state.processingRemainingTime = self.processingTime.getValue().evaluate()
            self.schedule(self.getTime())
            self._process(state)
        return state

    def _timeAdvanceFunction(self, state: ServerState) -> float:
        return state.processingRemainingTime.getValue()

    def _outputFunction(self, state: ServerState) -> Any:
        return state.outputBuffer.empty()

    def getProperties(self) -> EntityProperties:
        return {

        }

    @property
    def processingTime(self):
        return self._processingTime

    @processingTime.setter
    def processingTime(self, value: Union[ExpressionProperty, Expression]):
        if isinstance(value, ExpressionProperty):
            self._processingTime = value
        else:
            self._processingTime = ExpressionProperty(value)

    def getState(self) -> ServerState:
        """Returns the current state"""
        return super(Server, self).getState()
