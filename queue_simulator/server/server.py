from typing import Any, List, Union, Dict

from core.entity.core import Entity, EntityProperties, EntityManager
from core.entity.properties import ExpressionProperty, NumberProperty
from core.expresions.expression import Expression
from core.mathematics.values.value import Value
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.buffer.buffers import InputBuffer, OutputBuffer, ProcessBuffer
from queue_simulator.server.server_state import ServerState
from queue_simulator.shared.models import SerializableComponent


class Server(DiscreteEventModel, SerializableComponent):
    """Server of processes"""

    _processing_time: ExpressionProperty
    """Processing time of the server."""

    _initial_capacity: NumberProperty
    """Initial capacity of the process buffer."""

    _is_busy: bool
    """Processing time of the server."""

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem,
                 name: str,
                 processing_time: Union[ExpressionProperty, Expression] = Value(1),
                 initial_capacity: NumberProperty = NumberProperty(1),
                 entity_manager: EntityManager = None):
        super().__init__(dynamic_system,
                         name,
                         ServerState(
                             InputBuffer(name, entity_manager=entity_manager),
                             OutputBuffer(name, entity_manager=entity_manager),
                             ProcessBuffer(name, capacity=initial_capacity, entity_manager=entity_manager)
                         ),
                         entity_manager=entity_manager
                         )
        self.initial_capacity = initial_capacity
        self.processing_time = processing_time
        self._is_busy = False

    def _process(self, state: ServerState):
        for i in range(state.input_buffer.current_number_of_entities):
            if not state.process_buffer.is_full:
                time_to_be_scheduled = self.get_time()
                state.process_buffer.add([state.input_buffer.pop()], [time_to_be_scheduled])
                self.schedule(time_to_be_scheduled)
                self._is_busy = True
            else:
                break

    def _internal_state_transition_function(self, state: ServerState) -> ServerState:
        self._is_busy = False
        self._process(state)
        return state

    def _external_state_transition_function(self, state: ServerState,
                                            inputs: Dict[str, List[Entity]],
                                            event_time: Time) -> ServerState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.input_buffer.add(r_inputs)
        if len(r_inputs) > 0:
            state.process_buffer.decrease_time(event_time)
            self._process(state)
        return state

    def _time_advance_function(self, state: ServerState) -> Time:
        return self.processing_time.get_value().evaluate()

    def _output_function(self, state: ServerState) -> Any:
        state.output_buffer.add(state.process_buffer.get_processed())
        return state.output_buffer.empty()

    def get_properties(self) -> EntityProperties:
        return {

        }

    @property
    def processing_time(self):
        return self._processing_time

    @processing_time.setter
    def processing_time(self, value: Union[ExpressionProperty, Expression]):
        if isinstance(value, ExpressionProperty):
            self._processing_time = value
        else:
            self._processing_time = ExpressionProperty(value)

    @property
    def initial_capacity(self):
        return self._processing_time

    @initial_capacity.setter
    def initial_capacity(self, value: NumberProperty):
        self._initial_capacity = value
        self.get_state().process_buffer.capacity = value

    def get_state(self) -> ServerState:
        """Returns the current state"""
        return super(Server, self).get_state()

    def __str__(self):
        return self.get_id()
