from typing import List, Optional, Union

from core.entity.core import EntityEmitter, EntityProperties, Entity
from core.entity.properties import ExpressionProperty, AnyProperty
from core.expresions import Expression
from core.types.model_input import ModelInput

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.buffer.buffers import OutputBuffer

from queue_simulator.source import SourceProperty, SourceState


# https://simulemos.cl/books/simio/page/source
class Source(DiscreteEventModel):
    """Source of entities"""
    entityNumber = 0

    _interArrivalTime: Optional[ExpressionProperty]
    """InterArrival time of the entities"""

    _entitiesPerArrival: Optional[ExpressionProperty]
    """Entities created per arrival"""

    _entityEmitter: Optional[AnyProperty[EntityEmitter]]
    """Emitter of entities"""

    def get_properties(self) -> EntityProperties:
        return {
            SourceProperty.ENTITY_TYPE: self.entity_emitter,
            SourceProperty.INTER_ARRIVAL_TIME: self.inter_arrival_time
        }

    def __init__(self,
                 dynamic_system: DiscreteEventDynamicSystem,
                 name: str,
                 entity_emitter: Union[EntityEmitter, AnyProperty[EntityEmitter]] = None,
                 inter_arrival_time: Union[Expression, ExpressionProperty] = None,
                 entities_per_arrival: Union[Expression, ExpressionProperty] = None,
                 ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            entity_emitter (EntityEmitter): Emitter of entities.
            inter_arrival_time (ExpressionProperty): InterArrival time of the entities.
        """
        super().__init__(dynamic_system, name, SourceState(OutputBuffer(name)))
        self.inter_arrival_time = inter_arrival_time
        self.entity_emitter = entity_emitter
        self.entities_per_arrival = entities_per_arrival

    def __are_valid_properties(self):
        """Checks if the properties are valid"""
        return not (self.inter_arrival_time is None or
                    self.entity_emitter is None or
                    self.entities_per_arrival is None)

    def _internal_state_transition_function(self, state: SourceState) -> SourceState:
        """Creates an entity
        Args:
            state (SourceState): Current state of the model.
        """
        if self.__are_valid_properties():
            entities = []
            for i in range(self.entities_per_arrival.get_value().evaluate()):
                entities.append(self.entity_emitter.get_value().generate())
            state.outputBuffer.add(entities)
            self.schedule(self.get_time())
        return state

    def _external_state_transition_function(self, state: SourceState, inputs: ModelInput,
                                            event_time: float) -> SourceState:
        """Returns the current state
        Args:
            state (SourceState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        return state

    def _time_advance_function(self, state: SourceState) -> float:
        """Time for an autonomous event.
        Args:
            state (SourceState): Current state of the model.
        """
        if self.inter_arrival_time is not None:
            return max(self.inter_arrival_time.get_value().evaluate(), 0.00001)
        return 0

    def _output_function(self, state: SourceState) -> List[Entity]:
        """Return the entities created.
        Args:
            state (SourceState):
        """
        return state.outputBuffer.empty()

    @property
    def inter_arrival_time(self):
        return self._interArrivalTime

    @inter_arrival_time.setter
    def inter_arrival_time(self, value: Union[Expression, ExpressionProperty]):
        if isinstance(value, ExpressionProperty):
            self._interArrivalTime = value
        else:
            self._interArrivalTime = ExpressionProperty(value)
        self.schedule(self.get_time())

    @property
    def entity_emitter(self):
        return self._entityEmitter

    @entity_emitter.setter
    def entity_emitter(self, value: Union[EntityEmitter, AnyProperty[EntityEmitter]]):
        if isinstance(value, AnyProperty):
            self._entityEmitter = value
        else:
            self._entityEmitter = AnyProperty(value)

    @property
    def entities_per_arrival(self):
        return self._entitiesPerArrival

    @entities_per_arrival.setter
    def entities_per_arrival(self, value: Expression):
        if isinstance(value, ExpressionProperty):
            self._entitiesPerArrival = value
        else:
            self._entitiesPerArrival = ExpressionProperty(value)

    def get_state(self) -> SourceState:
        """Returns the current state"""
        return super(Source, self).get_state()
