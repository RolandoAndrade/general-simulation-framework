from __future__ import annotations

from abc import ABC
from decimal import Decimal
from random import shuffle, randint
from typing import List, Optional

from core.entity.core import Entity, EntityProperties, EntityManager
from core.entity.properties import NumberProperty, StringProperty
from queue_simulator.buffer.core import BufferPolicy, BufferProperty
from queue_simulator.shared.stats import StatSource, DataSource, ItemStats, Stat


class Buffer(Entity, StatSource, ABC):
    """Buffer of entities"""

    _content: List[Entity]
    """Content of the buffer"""

    capacity: NumberProperty[float]
    """Capacity of the buffer"""

    policy: StringProperty
    """Policy of the buffer"""

    __number_entered: NumberProperty[int]
    """Number of entities that entered into the buffer"""

    _in_station_history: List[int]
    """Number of entities in station history."""

    def __init__(
            self,
            name: str,
            capacity: NumberProperty[float] = NumberProperty(Decimal("inf")),
            policy: StringProperty = StringProperty(str(BufferPolicy.FIFO)),
            entity_manager: EntityManager = None,
    ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
            policy (StringProperty): Policy of the buffer.
        """
        super().__init__(name, entity_manager)
        self.capacity = capacity
        self._content = []
        self.policy = policy
        self.__number_entered = NumberProperty(0)
        self._in_station_history = []

    def add(self, entities: List[Entity], *args, **kwargs) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entities: Entities to be added.
        """
        quantity = len(entities)
        r_quantity = int(min(self.remaining_capacity.get_value(), quantity))
        self.__number_entered += r_quantity
        for i in range(r_quantity):
            self._content.append(entities[i])
        self._in_station_history.append(len(self._content))
        return quantity - r_quantity

    def get_content(self) -> List[Entity]:
        """Gets the content of the buffer"""
        if self.policy.get_value() == BufferPolicy.FIFO:
            return self._content
        elif self.policy.get_value() == BufferPolicy.LIFO:
            return self._content[::-1]
        random_order = self._content.copy()
        shuffle(random_order)
        return random_order

    def empty(self) -> List[Entity]:
        """Gets the content of the buffer and empties the buffer"""
        data = self._content.copy()
        self._content = []
        if self.policy.get_value() == BufferPolicy.FIFO:
            return data
        elif self.policy.get_value() == BufferPolicy.LIFO:
            return data[::-1]
        random_order = data.copy()
        shuffle(random_order)
        return random_order

    def pop(self) -> Optional[Entity]:
        """Pops the next element in the buffer"""
        if self.current_number_of_entities > 0:
            if self.policy.get_value() == BufferPolicy.FIFO:
                return self._content.pop(0)
            elif self.policy.get_value() == BufferPolicy.LIFO:
                return self._content.pop()
            return self._content.pop(randint(0, self.current_number_of_entities - 1))
        return None

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            BufferProperty.CAPACITY: self.capacity,
            BufferProperty.POLICY: self.policy,
            BufferProperty.NUMBER_ENTERED: self.number_entered,
        }

    @property
    def current_number_of_entities(self):
        """Returns the current number of entities into the buffer"""
        return len(self._content)

    @property
    def remaining_capacity(self):
        """Returns the current number of entities capable to be appended into
        the buffer
        """
        return self.capacity - self.current_number_of_entities

    @property
    def is_empty(self):
        """Returns true if the buffer is empty"""
        return self.current_number_of_entities == 0

    @property
    def is_full(self):
        """Returns true if the buffer is empty"""
        return self.remaining_capacity.get_value() == 0

    @property
    def number_entered(self) -> NumberProperty[int]:
        """Returns true if the buffer is empty"""
        return self.__number_entered

    @number_entered.setter
    def number_entered(self, value):
        """Sets the number entered"""
        self.__number_entered = value

    def __str__(self):
        return str(
            dict(
                {
                    BufferProperty.CAPACITY: str(self.capacity),
                    BufferProperty.POLICY: str(self.policy),
                    BufferProperty.NUMBER_ENTERED: str(self.__number_entered),
                }
            )
        )

    def get_datasource(self) -> DataSource:
        return DataSource(self.get_id(), [
            ItemStats("Entered", [
                Stat("Total", self.number_entered.get_value())
            ]),
            ItemStats("NumberInStation", [
                Stat("Maximum", Decimal(max(self._in_station_history))),
                Stat("Minimum", Decimal(min(self._in_station_history))),
                Stat("Average", Decimal(sum(self._in_station_history) / max(1, len(self._in_station_history)))),
                Stat("Total", self.number_entered.get_value())
            ])
        ])
