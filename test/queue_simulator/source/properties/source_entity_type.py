from __future__ import annotations

from core.components.entity.entity_property import EntityProperty
from test.queue_simulator.source.properties.source_property_type import SourcePropertyType


class SourceEntityType(EntityProperty):
    def __init__(self, entity_name: str = None):
        super().__init__(SourcePropertyType.SOURCE_ENTITY_TYPE,
                         entity_name)

    def getValue(self) -> str:
        """Returns the value of the property"""
        return super(SourceEntityType, self).getValue()
