from __future__ import annotations

from abc import ABC
from random import shuffle, randint
from typing import List, Optional

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_emitter import EntityEmitter
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.number_property import NumberProperty
from core.components.entity.properties.string_property import StringProperty
from queue_simulator.buffer.core.buffer_policy import BufferPolicy
from queue_simulator.buffer.core.buffer_property import BufferProperty


class Buffer(Entity, ABC):
    """Buffer of entities"""

    _content: List[Entity]
    """Content of the buffer"""

    capacity: NumberProperty[float]
    """Capacity of the buffer"""

    policy: StringProperty
    """Policy of the buffer"""

    numberEntered: NumberProperty[int]
    """Number of entities that entered into the buffer"""

    def __init__(self,
                 name: str,
                 capacity: NumberProperty[float] = NumberProperty(float("inf")),
                 policy: StringProperty = StringProperty(BufferPolicy.FIFO)):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
            policy (StringProperty): Policy of the buffer.
        """
        super().__init__(name)
        self.capacity = capacity
        self._content = []
        self.policy = policy
        self.numberEntered = NumberProperty(0)

    def add(self, entities: List[Entity]) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entities: Entities to be added.
        """
        quantity = len(entities)
        rQuantity = int(min(self.remainingCapacity, quantity))
        self.numberEntered += rQuantity
        for i in range(rQuantity):
            self._content.append(entities[i])
        return quantity - rQuantity

    def getContent(self) -> List[Entity]:
        """Gets the content of the buffer"""
        if self.policy == BufferPolicy.FIFO:
            return self._content
        elif self.policy == BufferPolicy.LIFO:
            return self._content[::-1]
        randomOrder = self._content.copy()
        shuffle(randomOrder)
        return randomOrder

    def empty(self) -> List[Entity]:
        """Gets the content of the buffer and empties the buffer"""
        data = self._content.copy()
        self._content = []
        if self.policy == BufferPolicy.FIFO:
            return data
        elif self.policy == BufferPolicy.LIFO:
            return data[::-1]
        randomOrder = data.copy()
        shuffle(randomOrder)
        return randomOrder

    def pop(self) -> Optional[Entity]:
        """Pops the next element in the buffer"""
        if self.currentNumberOfEntities > 0:
            if self.policy == BufferPolicy.FIFO:
                return self._content.pop(0)
            elif self.policy == BufferPolicy.LIFO:
                return self._content.pop()
            return self._content.pop(randint(0, self.currentNumberOfEntities))
        return None

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            BufferProperty.CAPACITY: self.capacity,
            BufferProperty.POLICY: self.policy,
            BufferProperty.NUMBER_ENTERED: self.numberEntered
        }

    @property
    def currentNumberOfEntities(self):
        """Returns the current number of entities into the buffer"""
        return len(self._content)

    @property
    def remainingCapacity(self):
        """Returns the current number of entities capable to be appended into the buffer"""
        return self.capacity - self.currentNumberOfEntities

    @property
    def isEmpty(self):
        """Returns true if the buffer is empty"""
        return self.currentNumberOfEntities == 0

    @property
    def isFull(self):
        """Returns true if the buffer is empty"""
        return self.remainingCapacity == 0
