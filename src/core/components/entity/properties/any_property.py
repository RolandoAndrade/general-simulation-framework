from __future__ import annotations

from typing import Any

from core.components.entity.core.entity_property import EntityProperty
from core.components.entity.core.property_type import PropertyType


class AnyProperty(EntityProperty):
    def __init__(self, value: Any):
        super().__init__(value, PropertyType.ANY)
