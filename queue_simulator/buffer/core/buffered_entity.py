from __future__ import annotations

from core.entity.core import Entity, EntityProperties
from core.types import Time


class BufferedEntity(Entity):
    """Entity in queue"""

    _serial = 0
    """Serial of the entity"""

    _entity: Entity
    """Queued entity."""

    remaining_time: Time
    """Remaining time in queue."""

    def __init__(self, entity: Entity, remaining_time: Time):
        super().__init__("Buffered Entity " + str(BufferedEntity._serial))
        BufferedEntity._serial += 1
        self._entity = entity
        self.remaining_time = remaining_time

    def get_properties(self) -> EntityProperties:
        pass

    @property
    def entity(self) -> Entity:
        return self._entity
