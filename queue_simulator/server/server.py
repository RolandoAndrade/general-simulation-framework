from typing import Any, List, Union, Dict

from core.entity.core import Entity, EntityProperties
from core.expresions.expression import Expression

from core.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.models.discrete_event_model import DiscreteEventModel
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

    def _internal_state_transition_function(self, state: ServerState) -> ServerState:
        self._isBusy = False
        state.outputBuffer.add(state.processBuffer.empty())
        self._process(state)
        # recalculate the processing time
        state.processingRemainingTime = self.processingTime.get_value().evaluate()
        if self._isBusy:
            self.schedule(self.get_time())
        return state

    def _external_state_transition_function(self, state: ServerState,
                                            inputs: Dict[str, List[Entity]],
                                            event_time: float) -> ServerState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.inputBuffer.add(r_inputs)
        if not self._isBusy and len(r_inputs) > 0:
            state.processingRemainingTime = self.processingTime.get_value().evaluate()
            self.schedule(self.get_time())
            self._process(state)
        return state

    def _time_advance_function(self, state: ServerState) -> float:
        return state.processingRemainingTime.get_value()

    def _output_function(self, state: ServerState) -> Any:
        return state.outputBuffer.empty()

    def get_properties(self) -> EntityProperties:
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

    def get_state(self) -> ServerState:
        """Returns the current state"""
        return super(Server, self).get_state()
