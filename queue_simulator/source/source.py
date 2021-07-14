from typing import List, Optional

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_emitter import EntityEmitter
from core.components.entity.core.entity_property import EntityProperties, EntityProperty
from core.components.entity.properties.any_property import AnyProperty
from core.components.entity.properties.expression_property import ExpressionProperty
from core.components.expresions.expression import Expression
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from mathematics.values.numeric_value import NumericValue
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer

# https://simulemos.cl/books/simio/page/source
from queue_simulator.source.properties.source_property import SourceProperty
from queue_simulator.source.properties.source_state import SourceState


class Source(DiscreteEventModel):
    """Source of entities"""
    entityNumber = 0

    interArrivalTime: Optional[ExpressionProperty]
    """InterArrival time of the entities"""

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
                 entityEmitter: AnyProperty[EntityEmitter] = None,
                 interArrivalTime: ExpressionProperty = None,
                 ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            entityEmitter: Emitter of entities.
            interArrivalTime (ExpressionProperty): InterArrival time of the entities.
        """
        super().__init__(dynamic_system, name)
        self.setUpState(SourceState(OutputBuffer(name)))
        self.interArrivalTime = interArrivalTime
        self.entityEmitter = entityEmitter

    def __areValidProperties(self):
        """Checks if the properties are valid"""
        return not (self.interArrivalTime is None or
                    self.interArrivalTime is None)

    def _internalStateTransitionFunction(self, state: SourceState) -> ModelState:
        """Creates an entity
        Args:
            state (ModelState): Current state of the model.
        """
        if self.__areValidProperties():
            state.outputBuffer.add(self.entityEmitter.getValue(), self.interArrivalTime.getValue().evaluate())
        return state

    def _externalStateTransitionFunction(self, state: SourceState, inputs: ModelInput, event_time: float) -> ModelState:
        """Returns the current state
        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        return state

    def _timeAdvanceFunction(self, state: SourceState) -> float:
        """Time for an autonomous event.
        Args:
            state (ModelState):
        """
        return 1

    def _outputFunction(self, state: SourceState) -> List[Entity]:
        """Return the entities created.
        Args:
            state (ModelState):
        """
        return state.outputBuffer.empty()

    def getState(self) -> SourceState:
        """Returns the current state"""
        return super(Source, self).getState()
