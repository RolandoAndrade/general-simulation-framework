from typing import List, Optional

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_emitter import EntityEmitter
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.any_property import AnyProperty
from core.components.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.source.source_property import SourceProperty
from queue_simulator.source.source_state import SourceState


# https://simulemos.cl/books/simio/page/source

class Source(DiscreteEventModel):
    """Source of entities"""
    entityNumber = 0

    _interArrivalTime: Optional[ExpressionProperty]
    """InterArrival time of the entities"""

    entitiesPerArrival: Optional[ExpressionProperty]
    """Entities created per arrival"""

    entityEmitter: Optional[AnyProperty[EntityEmitter]]
    """Emitter of entities"""

    def getProperties(self) -> EntityProperties:
        return {
            SourceProperty.ENTITY_TYPE: self.entityEmitter,
            SourceProperty.INTER_ARRIVAL_TIME: self.interArrivalTime
        }

    def __init__(self,
                 dynamic_system: DiscreteEventDynamicSystem,
                 name: str,
                 entity_emitter: AnyProperty[EntityEmitter] = None,
                 inter_arrival_time: ExpressionProperty = None,
                 entities_per_arrival: ExpressionProperty = None,
                 ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            entity_emitter: Emitter of entities.
            inter_arrival_time (ExpressionProperty): InterArrival time of the entities.
        """
        super().__init__(dynamic_system, name, SourceState(OutputBuffer(name)))
        self.interArrivalTime = inter_arrival_time
        self.entityEmitter = entity_emitter
        self.entitiesPerArrival = entities_per_arrival


    def __areValidProperties(self):
        """Checks if the properties are valid"""
        return not (self.interArrivalTime is None or
                    self.entityEmitter is None or
                    self.entitiesPerArrival is None)

    def _internalStateTransitionFunction(self, state: SourceState) -> SourceState:
        """Creates an entity
        Args:
            state (SourceState): Current state of the model.
        """
        if self.__areValidProperties():
            entities = []
            for i in range(self.entitiesPerArrival.getValue().evaluate()):
                entities.append(self.entityEmitter.getValue().generate())
            state.outputBuffer.add(entities)
        return state

    def _externalStateTransitionFunction(self, state: SourceState, inputs: ModelInput,
                                         event_time: float) -> SourceState:
        """Returns the current state
        Args:
            state (SourceState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        return state

    def _timeAdvanceFunction(self, state: SourceState) -> float:
        """Time for an autonomous event.
        Args:
            state (SourceState): Current state of the model.
        """
        if self.interArrivalTime is not None:
            return max(self.interArrivalTime.getValue().evaluate(), 0.00001)
        return 0

    def _outputFunction(self, state: SourceState) -> List[Entity]:
        """Return the entities created.
        Args:
            state (SourceState):
        """
        return state.outputBuffer.empty()

    @property
    def interArrivalTime(self):
        return self._interArrivalTime

    @interArrivalTime.setter
    def interArrivalTime(self, value: ExpressionProperty):
        self._interArrivalTime = value
        self.schedule(self.getTime())

    def getState(self) -> SourceState:
        """Returns the current state"""
        return super(Source, self).getState()
