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

class SourceState:
    OutputBuffer: OutputBuffer



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
        super().__init__(dynamic_system, name)
        self.setUpState({
            "OutputBuffer": OutputBuffer(name)
        })
        self.interArrivalTime = interArrivalTime
        self.entityEmitter = entityEmitter

    def __areValidProperties(self):
        return not (self.interArrivalTime is None or
                    self.interArrivalTime is None)


    def _internalStateTransitionFunction(self, state: SourceState) -> ModelState:
        if self.__areValidProperties():
            outputBuffer: OutputBuffer = state['OutputBuffer']
            outputBuffer.add(self.entityEmitter.getValue())
        return state

    def _externalStateTransitionFunction(self, state: ModelState, inputs: ModelInput, event_time: float) -> ModelState:
        return state

    def _timeAdvanceFunction(self, state: ModelState) -> float:
        return 1

    def _outputFunction(self, state: ModelState) -> List[Entity]:
        return state['OutputBuffer']
