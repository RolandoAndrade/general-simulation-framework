from __future__ import annotations

from typing import List

import heapq
from core.entity.core import Entity, EntityManager
from core.entity.properties import NumberProperty, StringProperty
from core.types import Time
from queue_simulator.buffer.core import Buffer, BufferPolicy, BufferedEntity


class ProcessBuffer(Buffer):
    """Process buffer"""

    _content: List[BufferedEntity]

    def __init__(self, name: str,
                 capacity: NumberProperty = NumberProperty(float("inf")),
                 entity_manager: EntityManager = None
                 ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
        """
        super().__init__(name + ".ProcessBuffer", capacity, StringProperty(str(BufferPolicy.PARALLEL)), entity_manager)

    def process(self):
        entities = self.get_content()

    def add(self, entities: List[Entity], times: List[Time] = None, *args, **kwargs) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entities (Entity): Entities to be added.
            times (Time): Time for processing.
        """
        if times is None:
            times = map(lambda: Time(1), entities)
        for entity, time in zip(entities, times):
            heapq.heappush(self._content, BufferedEntity(entity, time))
        return 0

    def get_processed(self) -> List[Entity]:
        """Gets the content of the buffer and empties the buffer"""
        s = []
        time = self.get_time_of_next_entity()
        while len(self._content) > 0 and self._content[0].remaining_time == time:
            s.append(heapq.heappop(self._content).entity)
        self.decrease_time(time)
        return s

    def get_time_of_next_entity(self) -> Time:
        """Gets the time of the next event"""
        if not self.is_empty:
            return self._content[0].remaining_time
        return Time(0)

    def decrease_time(self, time: Time):
        """Gets the time of the next event"""
        for entity in self._content:
            entity.decrease_time(time)
