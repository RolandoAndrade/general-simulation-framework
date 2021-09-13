from typing import List, Optional, Union

from core.entity.core import EntityEmitter, EntityProperties, Entity
from core.entity.properties import ExpressionProperty, Property
from core.expresions import Expression
from core.mathematics.distributions import ExponentialDistribution
from core.mathematics.values.value import Value
from core.types import Time
from core.types.model_input import ModelInput

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.buffer.buffers import OutputBuffer
from queue_simulator.entities import Emitter
from queue_simulator.shared.models import SerializableComponent
from queue_simulator.shared.stats import Statistical, ComponentStats, DataSource, ItemStats

from queue_simulator.source import SourceProperty, SourceState

from core.entity.core import EntityManager


# https://simulemos.cl/books/simio/page/source
class Source(DiscreteEventModel, SerializableComponent, Statistical):
    """Source of entities"""

    __inter_arrival_time: Optional[ExpressionProperty]
    """InterArrival time of the entities"""

    __entities_per_arrival: Optional[ExpressionProperty]
    """Entities created per arrival"""

    __time_offset: Optional[ExpressionProperty]
    """Time until the first transition"""

    __used_offset: Optional[ExpressionProperty]
    """Time until the first transition"""

    __entity_emitter: Optional[Property[EntityEmitter]]
    """Emitter of entities"""

    __serial: int = 0

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        name: str,
        entity_emitter: Union[EntityEmitter, Property[EntityEmitter]] = None,
        inter_arrival_time: Union[
            Expression, ExpressionProperty
        ] = ExponentialDistribution(0.25),
        entities_per_arrival: Union[Expression, ExpressionProperty] = Value(1),
        time_offset: Union[Expression, ExpressionProperty] = Value(0),
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            entity_emitter (EntityEmitter): Emitter of entities.
            inter_arrival_time (ExpressionProperty): InterArrival time of the entities.
        """
        super().__init__(
            dynamic_system,
            name,
            SourceState(OutputBuffer(name, entity_manager=entity_manager)),
            entity_manager=entity_manager,
        )
        self.inter_arrival_time = inter_arrival_time
        self.entity_emitter = entity_emitter or Emitter(
            "EntityEmitter" + name, entity_manager
        )
        self.entities_per_arrival = entities_per_arrival
        self.time_offset = time_offset

    def __check_properties(self):
        """Checks if the properties are valid"""
        if self.inter_arrival_time.get_value() is None:
            raise AttributeError("Interarrival time cannot be None")
        elif self.entities_per_arrival.get_value() is None:
            raise AttributeError("Entities per arrival cannot be None")
        elif self.entity_emitter.get_value() is None:
            raise AttributeError("Entity entities cannot be None")

    def _internal_state_transition_function(self, state: SourceState) -> SourceState:
        """Creates an entity
        Args:
            state (SourceState): Current state of the model.
        """
        self.__check_properties()
        entities = []
        for i in range(self.entities_per_arrival.get_value().evaluate()):
            entities.append(self.entity_emitter.get_value().generate())
        state.output_buffer.add(entities)
        self.__used_offset = ExpressionProperty(Value(0))
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(
        self, state: SourceState, inputs: ModelInput, event_time: float
    ) -> SourceState:
        """Returns the current state
        Args:
            state (SourceState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        return state

    def _time_advance_function(self, state: SourceState) -> Time:
        """Time for an autonomous event.
        Args:
            state (SourceState): Current state of the model.
        """
        if self.inter_arrival_time is not None:
            return (
                self.inter_arrival_time.get_value().evaluate()
            )
        return Time(-1)

    def _output_function(self, state: SourceState) -> List[Entity]:
        """Return the entities created.
        Args:
            state (SourceState):
        """
        return state.output_buffer.empty()

    @property
    def inter_arrival_time(self):
        return self.__inter_arrival_time

    @inter_arrival_time.setter
    def inter_arrival_time(self, value: Union[Expression, ExpressionProperty]):
        if isinstance(value, ExpressionProperty):
            self.__inter_arrival_time = value
        else:
            self.__inter_arrival_time = ExpressionProperty(value)
        self.clear()

    @property
    def entity_emitter(self):
        return self.__entity_emitter

    @entity_emitter.setter
    def entity_emitter(self, value: Union[EntityEmitter, Property[EntityEmitter]]):
        if isinstance(value, Property):
            self.__entity_emitter = value
        else:
            self.__entity_emitter = Property(value)
        self.clear()

    @property
    def entities_per_arrival(self):
        return self.__entities_per_arrival

    @entities_per_arrival.setter
    def entities_per_arrival(self, value: Expression):
        if isinstance(value, ExpressionProperty):
            self.__entities_per_arrival = value
        else:
            self.__entities_per_arrival = ExpressionProperty(value)
        self.clear()

    @property
    def time_offset(self):
        return self.__time_offset

    @time_offset.setter
    def time_offset(self, value: Expression):
        if isinstance(value, ExpressionProperty):
            self.__time_offset = value
        else:
            self.__time_offset = ExpressionProperty(value)
        self.__used_offset = self.__time_offset
        self.clear()

    def get_state(self) -> SourceState:
        """Returns the current state"""
        return super(Source, self).get_state()

    def get_properties(self) -> EntityProperties:
        return {
            SourceProperty.ENTITY_TYPE: self.entity_emitter,
            SourceProperty.INTER_ARRIVAL_TIME: self.inter_arrival_time,
            SourceProperty.TIME_OFFSET: self.time_offset,
            SourceProperty.ENTITIES_PER_ARRIVAL: self.entities_per_arrival,
        }

    def clear(self):
        self.get_state().output_buffer.empty()
        self.unschedule()
        try:
            self.schedule(self.time_offset.get_value().evaluate())
        except AttributeError:
            self.schedule(Time(0))

    def init(self):
        pass

    def __str__(self):
        return self.get_id()

    def set_id(self, name: str):
        super(Source, self).set_id(name)
        try:
            self.get_state().rename(name)
        except AttributeError:
            pass

    def get_stats(self) -> ComponentStats:
        return ComponentStats("Source", self.get_id(), {
            self.get_state().output_buffer.get_datasource()
        })
