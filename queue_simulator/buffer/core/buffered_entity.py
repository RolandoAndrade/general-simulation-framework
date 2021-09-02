from __future__ import annotations

from core.entity.core import Entity, EntityProperties
from core.types import Time


class BufferedEntity(Entity):
    """Entity in queue"""

    _serial = 0
    """Serial of the entity"""

    _entity: Entity
    """Queued entity."""

    _remaining_time: Time
    """Remaining time in queue."""

    def __init__(self, entity: Entity, remaining_time: Time):
        super().__init__("Buffered Entity " + str(BufferedEntity._serial))
        BufferedEntity._serial += 1
        self._entity = entity
        self._remaining_time = remaining_time

    def get_properties(self) -> EntityProperties:
        pass

    @property
    def entity(self) -> Entity:
        return self._entity

    @property
    def remaining_time(self) -> Time:
        return self._remaining_time

    def decrease_time(self, time: Time) -> Time:
        self._remaining_time = max(self.remaining_time - time, Time(0))

    def __lt__(self, other: BufferedEntity):
        return self.remaining_time < other.remaining_time

    def __str__(self):
        return "BufferedEntity" + str(
            dict({"ID": self.get_id(), "remaining_time": str(self.remaining_time)})
        )
