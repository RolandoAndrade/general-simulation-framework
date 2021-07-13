from __future__ import annotations

from abc import ABC
from typing import List

from core.components.entity.core.entity import Entity
from core.components.entity.properties.number_property import NumberProperty
from core.components.entity.properties.string_property import StringProperty
from queue_simulator.buffer.core.buffer_policy import BufferPolicy


class Buffer(Entity, ABC):
    """Buffer of entities"""

    _content: List[Entity]
    """Content of the buffer"""

    capacity: NumberProperty
    """Capacity of the buffer"""

    policy: StringProperty
    """Policy of the buffer"""

    numberEntered: NumberProperty
    """Number of entities that entered into the buffer"""

    def __init__(self,
                 name: str,
                 capacity: NumberProperty = NumberProperty(float("inf")),
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

    def add(self, entity: Entity, quantity: int = 1) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entity (Entity): Entity to be created
            quantity (int):
        """
        capacity = self.capacity - len(self._content)
        rQuantity = int(min(capacity, quantity))
        self.numberEntered += rQuantity
        self._content += [entity] * rQuantity
        return quantity - rQuantity
