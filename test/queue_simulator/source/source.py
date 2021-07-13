from typing import List

from core.components.entity.core.entity import Entity
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from test.queue_simulator.buffer.output_buffer import OutputBuffer
from test.queue_simulator.source.properties.source_entity_type import SourceEntityType
from test.queue_simulator.source.properties.source_inter_arrival_time import SourceInterArrivalTime

# https://simulemos.cl/books/simio/page/source
from test.queue_simulator.source.properties.source_property_type import SourcePropertyType


class Source(DiscreteEventModel):
    entityNumber = 0

    def __init__(self,
                 dynamic_system: DiscreteEventDynamicSystem,
                 name: str):
        super().__init__(dynamic_system, name, properties={
            SourcePropertyType.SOURCE_ENTITY_TYPE: SourceEntityType(),
            SourcePropertyType.SOURCE_INTER_ARRIVAL_TIME: SourceInterArrivalTime(),
        })
        ob = OutputBuffer(dynamic_system, name, self.getTime())
        self.add(ob)
        self.setUpState({
            "OutputBuffer": ob
        })

    def add(self):

    def __areValidProperties(self):
        return not (self[SourcePropertyType.SOURCE_INTER_ARRIVAL_TIME].getValue() is None or
                    self[SourcePropertyType.SOURCE_ENTITY_TYPE].getValue() is None)

    def __getInterArrivalTime(self) -> float:
        return self[SourcePropertyType.SOURCE_INTER_ARRIVAL_TIME].getValue().evaluate()

    def __getEntityType(self) -> Entity:
        Source.entityNumber += 1
        return Entity("Entity" + str(Source.entityNumber))

    def _internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        if self.__areValidProperties():
            state['created_entities'] = self.__getInterArrivalTime()
            state['outputs'] += state['created_entities']
        return state

    def _externalStateTransitionFunction(self, state: ModelState, inputs: ModelInput, event_time: float) -> ModelState:
        return state

    def _timeAdvanceFunction(self, state: ModelState) -> float:
        return 1

    def _outputFunction(self, state: ModelState) -> List[Entity]:
        return [self.__getEntityType()] * state['created_entities']
