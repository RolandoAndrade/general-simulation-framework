from typing import Any, List, Union, Dict

from core.entity.core import Entity, EntityProperties
from core.entity.properties import ExpressionProperty
from core.expresions.expression import Expression
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.buffer.buffers import InputBuffer, OutputBuffer, ProcessBuffer
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
        self.processing_time = processing_time
        self._isBusy = False

    def _process(self, state: ServerState):
        for i in range(state.input_buffer.current_number_of_entities):
            if not state.process_buffer.is_full:
                state.process_buffer.add([state.input_buffer.pop()])
                self._isBusy = True
            else:
                break

    def _internal_state_transition_function(self, state: ServerState) -> ServerState:
        self._isBusy = False
        state.output_buffer.add(state.process_buffer.empty())
        self._process(state)
        # recalculate the processing time
        state.processing_remaining_time = self.processing_time.get_value().evaluate()
        if self._isBusy:
            self.schedule(self.get_time())
        return state

    def _external_state_transition_function(self, state: ServerState,
                                            inputs: Dict[str, List[Entity]],
                                            event_time: float) -> ServerState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.input_buffer.add(r_inputs)
        if not self._isBusy and len(r_inputs) > 0:
            state.processing_remaining_time = self.processing_time.get_value().evaluate()
            self.schedule(self.get_time())
            self._process(state)
        return state

    def _time_advance_function(self, state: ServerState) -> float:
        return state.processing_remaining_time.get_value()

    def _output_function(self, state: ServerState) -> Any:
        return state.output_buffer.empty()

    def get_properties(self) -> EntityProperties:
        return {

        }

    @property
    def processing_time(self):
        return self._processingTime

    @processing_time.setter
    def processing_time(self, value: Union[ExpressionProperty, Expression]):
        if isinstance(value, ExpressionProperty):
            self._processingTime = value
        else:
            self._processingTime = ExpressionProperty(value)

    def get_state(self) -> ServerState:
        """Returns the current state"""
        return super(Server, self).get_state()
