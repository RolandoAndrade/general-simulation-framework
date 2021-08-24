from __future__ import annotations

from typing import List

from core.entity.core import Entity
from core.entity.properties import NumberProperty, StringProperty
from core.types import Time
from queue_simulator.buffer.core import Buffer, BufferPolicy, BufferedEntity


class ProcessBuffer(Buffer):
    """Input buffer"""

    def __init__(self, name: str,
                 capacity: NumberProperty = NumberProperty(float("inf")),
                 policy: StringProperty = StringProperty(str(BufferPolicy.FIFO))
                 ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
            policy (StringProperty): Policy of the buffer.
        """
        super().__init__(name + ".ProcessBuffer", capacity, policy)

    def process(self):
        entities = self.get_content()

    def add(self, entities: List[Entity], times: List[Time]) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entities (Entity): Entities to be added.
            times (Time): Time for processing.
        """
        if self.policy == BufferPolicy.FIFO:
            last_time = 0
            if not self.is_empty:
                last_time = self._content[-1]
            times = map(lambda t: t + last_time, times)
        e = []
        for entity, time in zip(entities, times):
            e.append(BufferedEntity(entity, time))
        return super().add(e)

    def get_processed(self) -> List[Entity]:
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
