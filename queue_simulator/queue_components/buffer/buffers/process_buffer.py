from __future__ import annotations

from decimal import Decimal
from typing import List

import heapq
from core.entity.core import Entity, EntityManager
from core.entity.properties import NumberProperty, StringProperty
from core.types import Time
from queue_simulator.queue_components.buffer.core import (
    Buffer,
    BufferPolicy,
    BufferedEntity,
)
from queue_simulator.queue_components.shared.stats import DataSource, ItemStats, Stat


class ProcessBuffer(Buffer):
    """Process buffer"""

    _content: List[BufferedEntity]

    def __init__(
        self,
        name: str,
        capacity: NumberProperty = NumberProperty(Decimal("inf")),
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
        """
        super().__init__(
            name, capacity, StringProperty(str(BufferPolicy.PARALLEL)), entity_manager
        )
        self.__processing_time_history = []

    def process(self):
        entities = self.get_content()

    def add(
        self, entities: List[Entity], times: List[Time] = None, *args, **kwargs
    ) -> int:
        """Adds an element to the buffer and returns the number of elements that
        cannot be added because the buffer capacity

        Args:
            entities (Entity): Entities to be added.
            times (Time): Time for processing.
        """
        if times is None:
            times = map(lambda: Time(1), entities)
        for entity, time in zip(entities, times):
            if not self.is_full:
                heapq.heappush(self._content, BufferedEntity(entity, time))
            else:
                break
        quantity = len(entities)
        r_quantity = int(min(self.remaining_capacity.get_value(), quantity))
        self.number_entered += r_quantity
        self._in_station_history.append(len(self._content))
        return quantity - r_quantity

    def get_processed(self) -> List[Entity]:
        """Gets the content of the buffer and empties the buffer"""
        s = []
        time = self.get_time_of_next_entity()
        self.__processing_time_history.append(time)
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

    def set_id(self, name: str):
        super(ProcessBuffer, self).set_id(name + ".ProcessBuffer")

    def get_datasource(self) -> DataSource:
        ds = super(ProcessBuffer, self).get_datasource()
        ds.item_stats.append(
            ItemStats(
                "ProcessingTime",
                [
                    Stat("Maximum", max(self.__processing_time_history)),
                    Stat("Minimum", min(self.__processing_time_history)),
                    Stat(
                        "Average",
                        sum(self.__processing_time_history)
                        / max(1, len(self.__processing_time_history)),
                    ),
                    Stat("Total", sum(self.__processing_time_history)),
                ],
            )
        )
        return ds
